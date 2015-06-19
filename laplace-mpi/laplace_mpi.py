#! /usr/bin/env python

from sys import stdout
from time import time

import itertools as it

import numpy as np
from mpi4py import MPI

COLUMNS    =              1000
COLUMNS_P1 = COLUMNS    +    1
COLUMNS_P2 = COLUMNS_P1 +    1

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

ROWS       =              1000
START_ROW  = (ROWS*rank       )//size
END_ROW    = (ROWS*rank + ROWS)//size

LOCAL_ROWS = END_ROW - START_ROW
LOCAL_ROWS_P1 = LOCAL_ROWS    + 1
LOCAL_ROWS_P2 = LOCAL_ROWS_P1 + 1

MAX_TEMP_ERROR = 0.01
local_dt = np.empty(1)
global_dt = np.empty(1)
global_dt[0] = MAX_TEMP_ERROR*1.1

max_iterations = None
if rank == 0:
    max_iterations = int(raw_input('Maximum iterations [100-4000]?\n'))

# broadcast input to other ranks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

iteration = 1

if rank == 0:
    start_time = time()

# initialize Temperature and Temperature_last <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# do until error is minimal or until max steps
while ( global_dt[0] > MAX_TEMP_ERROR and iteration <= max_iterations ):
    # exchange boundary rows between adjacent ranks <<<<<<<<<<<<<<<<<<<<<<<<<<

    # main calculation: average my four neighbors
    Temperature[1:-1, 1:-1] = 0.25*(
        Temperature_last[2:  , 1:-1] +
        Temperature_last[ :-2, 1:-1] +
        Temperature_last[1:-1, 2:  ] +
        Temperature_last[1:-1,  :-2]
    )

    # compute local_dt[0] = maximum local difference <<<<<<<<<<<<<<<<<<<<<<<<<

    # parallel reduction of local_dt <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # copy grid to old grid for next iteration <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # periodically print test values
    if iteration % 100 == 0:
        # track progress
        gather_data = []
        for i in range(ROWS - 5, ROWS + 1):
            if (
                (START_ROW <= i and i < END_ROW) or
                (i == END_ROW and END_ROW == ROWS and rank == size - 1)
            ):
                gather_data.append([i, Temperature[i - START_ROW, i]])

        gather_data = comm.gather(gather_data, root=0)

        if rank == 0:
            gather_data = it.chain.from_iterable(gather_data)

            print('---------- Iteration number: %d ------------' % iteration)
            for i, value in gather_data:
                stdout.write('[%d,%d]: %5.2f  ' % (i, i, value))

            stdout.write('\n')
            stdout.flush()

    iteration += 1

    if top_send_request is not None: top_send_request.wait()
    if bottom_send_request is not None: bottom_send_request.wait()

if rank == 0:
    stop_time = time()
    elapsed_time = stop_time - start_time

    print('\nMax error at iteration %d was %f' % (iteration-1, global_dt[0]))
    print('Total time was %f seconds.\n' % elapsed_time)

