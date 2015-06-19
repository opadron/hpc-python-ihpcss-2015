#! /usr/bin/env python

from sys import stdout
from time import time

import numpy as np

COLUMNS    =              1000
COLUMNS_P1 = COLUMNS    +    1
COLUMNS_P2 = COLUMNS_P1 +    1

ROWS       =              1000
ROWS_P1    = ROWS       +    1
ROWS_P2    = ROWS_P1    +    1

MAX_TEMP_ERROR = 0.01
dt = MAX_TEMP_ERROR*1.1

max_iterations = int(raw_input('Maximum iterations [100-4000]?\n'))
iteration = 1

start_time = time()

# initialize Temperature_last and Temperature <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Temperature_last = np.zeros((ROWS_P2, COLUMNS_P2))
Temperature_last[:, -1] = (100.0/ROWS)*np.arange(ROWS_P2)
Temperature_last[-1, :] = (100.0/COLUMNS)*np.arange(COLUMNS_P2)

Temperature = np.empty_like(Temperature_last)

# do until error is minimal or until max steps
while ( dt > MAX_TEMP_ERROR and iteration <= max_iterations ):

    # main calculation: average my four neighbors <<<<<<<<<<<<<<<<<<<<<<<<<<<<
    Temperature[1:-1, 1:-1] = 0.25*(
        Temperature_last[2:  , 1:-1] +
        Temperature_last[ :-2, 1:-1] +
        Temperature_last[1:-1, 2:  ] +
        Temperature_last[1:-1,  :-2]
    )

    # compute dt = maximum difference <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    dt = np.max(np.fabs(
        Temperature[1:-1, 1:-1] - Temperature_last[1:-1, 1:-1]
    ))

    # copy grid to old grid for next iteration <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    Temperature_last[1:-1, 1:-1] = Temperature[1:-1, 1:-1]

    # periodically print test values
    if iteration % 100 == 0:
        # track progress
        print('---------- Iteration number: %d ------------' % iteration)

        for i in range(ROWS - 5, ROWS + 1):
            stdout.write('[%d,%d]: %5.2f  ' % (i, i, Temperature[i, i]))

        stdout.write('\n')
        stdout.flush()

    iteration += 1

stop_time = time()
elapsed_time = stop_time - start_time

print('\nMax error at iteration %d was %f' % (iteration-1, dt))
print('Total time was %f seconds.\n' % elapsed_time)

