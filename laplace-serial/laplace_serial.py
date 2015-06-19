#! /usr/bin/env python

import math
import sys

import itertools as it

from array import array
from time import time

COLUMNS = 1000
ROWS = 1000

MAX_TEMP_ERROR = 0.01

num_elements = (COLUMNS + 2)*(ROWS + 2)

iteration = 1
dt = 100

max_iterations = int(raw_input('Maximum iterations [100-4000]?\n'))

start_time = time()

# initialize
Temperature_last = array('d', it.repeat(0.0, num_elements))

# not necessary -- arrays already initialized to 0.0
# Temperature_last[::COLUMNS + 2] = array('d', it.repeat(0.0, ROWS + 2))

Temperature_last[COLUMNS + 1::COLUMNS + 2] = array(
    'd',
    ((100.0/ROWS)*i for i in range(ROWS + 2))
)

# not necessary -- arrays already initialized to 0.0
# Temperature_last[:COLUMNS + 2] = array('d', it.repeat(0.0, ROWS + 2))

start_index = (ROWS + 1)*(COLUMNS + 2)
end_index = start_index + COLUMNS + 2

Temperature_last[start_index:end_index] = array(
    'd',
    ((100.0/COLUMNS)*j for j in range(COLUMNS + 2))
)

Temperature = array('d', Temperature_last)

# do until error is minimal or until max steps
while ( dt > MAX_TEMP_ERROR and iteration <= max_iterations ):
    # main calculation: average my four neighbors
    for i in range(1, ROWS + 1):
        start_index = i*(COLUMNS + 2) + 1
        end_index = start_index + COLUMNS

        Temperature[start_index:end_index] = array('d', (
            0.25*(
                Temperature_last[(i + 1)*(COLUMNS + 2) + j    ] +
                Temperature_last[(i - 1)*(COLUMNS + 2) + j    ] +
                Temperature_last[(i    )*(COLUMNS + 2) + j + 1] +
                Temperature_last[(i    )*(COLUMNS + 2) + j - 1]
            )
            for j in range(1, COLUMNS + 1)
        ))

    dt = max(
        max(
            math.fabs(
                Temperature[i*(COLUMNS + 2) + j] -
                Temperature_last[i*(COLUMNS + 2) + j]
            )
            for j in range(1, COLUMNS + 1)
        )
        for i in range(1, ROWS + 1)
    )

    # copy grid to old grid for next iteration
    Temperature_last[:] = Temperature

    # periodically print test values
    if iteration % 1 == 0:
        # track progress
        print('---------- Iteration number: %d ------------' % iteration)

        for i in range(ROWS - 5, ROWS + 1):
            sys.stdout.write(
                '[%d,%d]: %5.2f  ' % (
                    i, i, Temperature[i*(COLUMNS + 2) + i]
                )
            )

        sys.stdout.write('\n')
        sys.stdout.flush()

    iteration += 1

stop_time = time()

elapsed_time = stop_time - start_time

print('\nMax error at iteration %d was %f' % (iteration-1, dt))
print('Total time was %f seconds.\n' % elapsed_time)

