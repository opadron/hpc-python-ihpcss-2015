
from sys import stdout
from time import time

import itertools as it

from libc.math cimport fabs, fmax

import numpy as np
cimport numpy as np

from mpi4py import MPI
from mpi4py cimport MPI
from mpi4py.mpi_c cimport *

def main():
    cdef unsigned int COLUMNS    =              1000
    cdef unsigned int COLUMNS_P1 = COLUMNS    +    1
    cdef unsigned int COLUMNS_P2 = COLUMNS_P1 +    1

    cdef unsigned int i, j

    cdef MPI_Comm comm = MPI_COMM_WORLD
    cdef MPI_Status stat

    cdef int rank, size
    MPI_Comm_size(comm, &size)
    MPI_Comm_rank(comm, &rank)

    cdef unsigned int ROWS       = 1000
    cdef unsigned int START_ROW  = (ROWS*rank       )//size
    cdef unsigned int END_ROW    = (ROWS*rank + ROWS)//size

    cdef unsigned int LOCAL_ROWS    = END_ROW - START_ROW
    cdef unsigned int LOCAL_ROWS_P1 = LOCAL_ROWS    + 1
    cdef unsigned int LOCAL_ROWS_P2 = LOCAL_ROWS_P1 + 1

    cdef double MAX_TEMP_ERROR = 0.01
    cdef double local_dt, global_dt = 1.1*MAX_TEMP_ERROR

    cdef int max_iterations
    if rank == 0:
        max_iterations = <int>int(
            raw_input('Maximum iterations [100-4000]?\n'
        ))

    # broadcast input to other ranks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    cdef unsigned int iteration = 1

    cdef double start_time
    if rank == 0:
        start_time = time()

    # initialize Temperature and Temperature_last <<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # do until error is minimal or until max steps
    while ( global_dt > MAX_TEMP_ERROR and iteration <= max_iterations ):
        # exchange boundary rows between adjacent ranks <<<<<<<<<<<<<<<<<<<<<<

        local_dt = 0.0

        # main calculation: average my four neighbors
        for i in xrange(1, LOCAL_ROWS_P1):
            for j in xrange(1, COLUMNS_P1):
                Temperature[i, j] = 0.25*(
                    Temperature_last[i+1, j  ] +
                    Temperature_last[i-1, j  ] +
                    Temperature_last[i  , j+1] +
                    Temperature_last[i  , j-1]
                )

                local_dt = fmax(
                    local_dt,
                    fabs(Temperature[i, j] - Temperature_last[i, j]
                ))

        # parallel reduction of local_dt <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # copy grid to old grid for next iteration <<<<<<<<<<<<<<<<<<<<<<<<<<<

        # periodically print test values
        if iteration % 100 == 0:
            # track progress
            gather_data = []
            for i in range(ROWS - 5, ROWS + 1):
                if (
                    (START_ROW <= i and i < END_ROW) or
                    (i == END_ROW and END_ROW == ROWS and rank == size - 1)
                ):
                    gather_data.append((
                        i, Temperature[i - START_ROW, i]
                    ))

            gather_data = MPI.COMM_WORLD.gather(gather_data, root=0)

            if rank == 0:
                gather_data = it.chain.from_iterable(gather_data)

                print('---------- Iteration number: %d ------------' % iteration)
                for _i, value in gather_data:
                    stdout.write('[%d,%d]: %5.2f  ' % (_i, _i, value))

                stdout.write('\n')
                stdout.flush()

        iteration += 1

        if rank != 0: MPI_Wait(&top_send_request, &stat)
        if rank != size - 1: MPI_Wait(&bottom_send_request, &stat)

    cdef double stop_time, elapsed_time
    if rank == 0:
        stop_time = time()
        elapsed_time = stop_time - start_time

        print('\nMax error at iteration %d was %f' % (iteration - 1, global_dt))
        print('Total time was %f seconds.\n' % elapsed_time)

if __name__ == '__main__':
    main()

