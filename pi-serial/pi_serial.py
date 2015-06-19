#! /usr/bin/env python

from time import time
from sys import stdout
from math import pi, sqrt, fabs

N = int(raw_input('Maximum number of terms?\n'))

update_frequency = 1000000

start_time = time()
partial_sum = 0.0
for i in xrange(1, N + 1):
    partial_sum += (1.0/i)/i

    if i % update_frequency == 0:
        partial_result = sqrt(6*partial_sum)
        partial_error = fabs(pi - partial_result)
        print('partial error: %e' % partial_error)
        stdout.flush()

stop_time = time()
elapsed_time = stop_time - start_time

partial_result = sqrt(6*partial_sum)
partial_error = fabs(pi - partial_result)

print('\nPartial error after %d terms was %e' % (N, partial_error))
print('Total time was %f seconds.\n' % elapsed_time)

