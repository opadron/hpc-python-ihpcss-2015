#! /usr/bin/env python

from time import time
from sys import stdout
from math import pi, sqrt, fabs

import numpy as np

N = int(raw_input('Maximum number of terms?\n'))

update_frequency = 1000000
num_iterations = N//update_frequency
num_left_over_iterations = N % update_frequency

start_time = time()

# initialize array <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
array = np.empty((update_frequency,))

partial_sum = 0.0

range_start = 1
range_stop = range_start + update_frequency

for i in xrange(num_iterations):
    # main array computation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    array[:] = np.arange(range_start, range_stop)
    array[:] = (1.0/array)/array

    # compute partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    partial_sum += np.sum(array)

    range_start += update_frequency
    range_stop += update_frequency

    partial_result = sqrt(6*partial_sum)
    partial_error = fabs(pi - partial_result)
    print('partial error: %e' % partial_error)
    stdout.flush()

if num_left_over_iterations > 0:
    # left over array computation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    nloi = num_left_over_iterations
    array[:nloi] = np.arange(range_start, range_start + nloi)

    array[:nloi] = ( 1.0/array[:nloi] )/array[:nloi]

    # left over partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    partial_sum += np.sum(array[:nloi])

stop_time = time()
elapsed_time = stop_time - start_time

partial_result = sqrt(6*partial_sum)
partial_error = fabs(pi - partial_result)

print('\nPartial error after %d terms was %e' % (N, partial_error))
print('Total time was %f seconds.\n' % elapsed_time)

