#! /usr/bin/env python

import math
import sys

from time import time
from math import pi, sqrt, fabs

import numpy as np

from mpi4py import MPI

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

N = None
if rank == 0:
    N = int(raw_input('Maximum number of terms?\n'))

N = comm.bcast(N, root=0)

start_N = (rank*N)//size
end_N = (rank*N + N)//size
local_N = end_N - start_N

update_frequency = 1000000
num_iterations = local_N//update_frequency
num_left_over_iterations = local_N % update_frequency

if rank == 0:
    start_time = time()

array = np.empty((update_frequency,))

local_partial_sum = np.empty((1,))
partial_sum = np.empty((1,))

local_partial_sum[0] = 0.0

range_start = start_N + 1
range_stop = range_start + update_frequency

for i in xrange(num_iterations):
    array[:] = np.arange(range_start, range_stop)
    array[:] = 1.0/(array*array)

    local_partial_sum[0] += np.sum(array)

    range_start += update_frequency
    range_stop += update_frequency

    comm.Reduce(local_partial_sum, partial_sum, op=MPI.SUM, root=0)

    if rank == 0:
        partial_result = sqrt(6*partial_sum[0])
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
    local_partial_sum[0] += np.sum(array[slice])

comm.Reduce(local_partial_sum, partial_sum, op=MPI.SUM, root=0)

if rank == 0:
    stop_time = time()

    elapsed_time = stop_time - start_time

    partial_result = sqrt(6*partial_sum[0])
    partial_error = fabs(pi - partial_result)

    print('\nMax error with %d terms was %e' % (N, partial_error))
    print('Total time was %f seconds.\n' % elapsed_time)

