#! /usr/bin/env python

from sys import stdout
from time import time
from math import fabs

COLUMNS    =              1000
COLUMNS_P1 = COLUMNS    +    1
COLUMNS_P2 = COLUMNS_P1 +    1

ROWS       =              1000
ROWS_P1    = ROWS       +    1
ROWS_P2    = ROWS_P1    +    1

MAX_TEMP_ERROR = 0.01

iteration = 1
dt = 100

max_iterations = int(raw_input('Maximum iterations [100-4000]?\n'))

start_time = time()

# initialize
Temperature_last = [
    [ 0.0 for i in range(COLUMNS_P2) ]
    for j in range(ROWS_P2)
]

Temperature = [
    [ 0.0 for i in range(COLUMNS_P2) ]
    for j in range(ROWS_P2)
]

for i in range(ROWS_P2):
    Temperature_last[i][-1] = (100.0/ROWS)*i

for j in range(COLUMNS_P1):
    Temperature_last[-1][j] = (100.0/COLUMNS)*j

# do until error is minimal or until max steps
while ( dt > MAX_TEMP_ERROR and iteration <= max_iterations ):
    dt = 0.0

    # main calculation: average my four neighbors
    for i in range(1, ROWS_P1):
        for j in range(1, COLUMNS_P1):
            Temperature[i][j] = 0.25*(
                Temperature_last[i + 1][j    ] +
                Temperature_last[i - 1][j    ] +
                Temperature_last[i    ][j + 1] +
                Temperature_last[i    ][j - 1]
            )

            dt = max(dt, fabs(Temperature[i][j] - Temperature_last[i][j]))

    # copy grid to old grid for next iteration
    for i in range(1, ROWS_P1):
        for j in range(1, COLUMNS_P1):
            Temperature_last[i][j] = Temperature[i][j]

    # periodically print test values
    if iteration % 1 == 0:
        # track progress
        print('---------- Iteration number: %d ------------' % iteration)

        for i in range(ROWS - 5, ROWS + 1):
            stdout.write('[%d,%d]: %5.2f  ' % (i, i, Temperature[i][i]))

        stdout.write('\n')
        stdout.flush()

    iteration += 1

stop_time = time()

elapsed_time = stop_time - start_time

print('\nMax error at iteration %d was %f' % (iteration-1, dt))
print('Total time was %f seconds.\n' % elapsed_time)

