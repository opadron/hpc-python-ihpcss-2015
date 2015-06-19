#! /usr/bin/env python

import math
import sys

import numpy as np
from time import time

COLUMNS    =              1000
ROWS       =              1000
COLUMNS_P1 = COLUMNS    +    1
ROWS_P1    = ROWS       +    1
COLUMNS_P2 = COLUMNS_P1 +    1
ROWS_P2    = ROWS_P1    +    1

MAX_TEMP_ERROR = 0.01
dt = MAX_TEMP_ERROR*1.1

shape = (ROWS_P2, COLUMNS_P2)

max_iterations = int(raw_input('Maximum iterations [100-4000]?\n'))
iteration = 1

start_time = time()

# initialize
Temperature_last = np.zeros(shape)
Temperature_last[:, -1] = (100.0/ROWS)*np.r_[:ROWS + 2]
Temperature_last[-1, :] = (100.0/COLUMNS)*np.r_[:COLUMNS + 2]

Temperature = np.empty_like(Temperature_last)

# do until error is minimal or until max steps
while ( dt > MAX_TEMP_ERROR and iteration <= max_iterations ):
    # main calculation: average my four neighbors
    Temperature[1:-1, 1:-1] = 0.25*(
        Temperature_last[2:  , 1:-1] +
        Temperature_last[ :-2, 1:-1] +
        Temperature_last[1:-1, 2:  ] +
        Temperature_last[1:-1,  :-2]
    )

    dt = np.max(np.fabs(
        Temperature[1:-1, 1:-1] - Temperature_last[1:-1, 1:-1]
    ))

    # copy grid to old grid for next iteration
    Temperature_last[1:-1, 1:-1] = Temperature[1:-1, 1:-1]

    # periodically print test values
    if iteration % 100 == 0:
        # track progress
        print('---------- Iteration number: %d ------------' % iteration)

        for i in range(ROWS - 5, ROWS + 1):
            sys.stdout.write(
                '[%d,%d]: %5.2f  ' % (
                    i, i, Temperature[i, i]
                )
            )

        sys.stdout.write('\n')
        sys.stdout.flush()

    iteration += 1

stop_time = time()

elapsed_time = stop_time - start_time

print('\nMax error at iteration %d was %f' % (iteration-1, dt))
print('Total time was %f seconds.\n' % elapsed_time)

