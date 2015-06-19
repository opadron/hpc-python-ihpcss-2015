#! /usr/bin/env python

import math
import sys

from time import time
from math import pi, sqrt, fabs

import numpy as np

N = int(raw_input('Maximum number of terms?\n'))

update_frequency = 1000000
num_iterations = N//update_frequency
num_left_over_iterations = N % update_frequency

start_time = time()

array = np.empty((update_frequency,))

partial_sum = 0.0

range_start = 1
range_stop = range_start + update_frequency

for i in xrange(num_iterations):
    array[:] = np.arange(range_start, range_stop)
    array[:] = 1.0/(array*array)

    partial_sum += np.sum(array)

    range_start += update_frequency
    range_stop += update_frequency

    partial_result = sqrt(6*partial_sum)
    partial_error = fabs(pi - partial_result)
    print('partial error: %e' % partial_error)
    sys.stdout.flush()

if num_left_over_iterations > 0:
    slice = Slice(None, num_left_over_iterations)
    array[slice] = np.arange(
        range_start,
        range_start + num_left_over_iterations
    )

    array[slice] = 1.0/(array[slice]*array[slice])
    partial_sum += np.sum(array[slice])

stop_time = time()

elapsed_time = stop_time - start_time

partial_result = sqrt(6*partial_sum)
partial_error = fabs(pi - partial_result)

print('\nMax error with %d terms was %e' % (N, partial_error))
print('Total time was %f seconds.\n' % elapsed_time)

