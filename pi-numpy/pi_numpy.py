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

partial_sum = 0.0

range_start = 1
range_stop = range_start + update_frequency

for i in xrange(num_iterations):
    # main array computation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # compute partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    partial_result = sqrt(6*partial_sum)
    partial_error = fabs(pi - partial_result)
    print('partial error: %e' % partial_error)
    stdout.flush()

if num_left_over_iterations > 0:
    # left over array computation <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # left over partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

stop_time = time()
elapsed_time = stop_time - start_time

partial_result = sqrt(6*partial_sum)
partial_error = fabs(pi - partial_result)

print('\nPartial error after %d terms was %e' % (N, partial_error))
print('Total time was %f seconds.\n' % elapsed_time)

