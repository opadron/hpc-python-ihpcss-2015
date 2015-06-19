#! /usr/bin/env python

from time import time
from sys import stdout
from math import pi, sqrt, fabs

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

N = None
if rank == 0:
    N = int(raw_input('Maximum number of terms?\n'))

# broadcast input to other ranks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

start_N = (rank*N    )//size
end_N   = (rank*N + N)//size
local_N = end_N - start_N

update_frequency = 1000000
num_iterations = local_N//update_frequency
num_left_over_iterations = local_N % update_frequency

if rank == 0:
    start_time = time()

# initialize array <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

local_partial_sum = np.empty((1,))
partial_sum = np.empty((1,))

local_partial_sum[0] = 0.0

range_start = start_N + 1
range_stop = range_start + update_frequency

for i in xrange(num_iterations):
    array[:] = np.arange(range_start, range_stop)
    array[:] = (1.0/array)/array

    local_partial_sum[0] += np.sum(array)

    range_start += update_frequency
    range_stop += update_frequency

    # parallel reduction of partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    if rank == 0:
        partial_result = sqrt(6*partial_sum[0])
        partial_error = fabs(pi - partial_result)
        print('partial error: %e' % partial_error)
        stdout.flush()

if num_left_over_iterations > 0:
    nloi = num_left_over_iterations
    array[:nloi] = np.arange(range_start, range_start + nloi)

    array[:nloi] = 1.0/(array[:nloi]*array[:nloi])
    local_partial_sum[0] += np.sum(array[:nloi])

# left over parallel reduction of partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

if rank == 0:
    stop_time = time()

    elapsed_time = stop_time - start_time

    partial_result = sqrt(6*partial_sum[0])
    partial_error = fabs(pi - partial_result)

    print('\nPartial error after %d terms was %e' % (N, partial_error))
    print('Total time was %f seconds.\n' % elapsed_time)

