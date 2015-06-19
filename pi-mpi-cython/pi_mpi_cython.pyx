
#cython: cdivision=True

from time import time
from sys import stdout

from libc.math cimport sqrt, fabs

from math import pi as python_pi
cdef double pi = python_pi

from mpi4py import MPI
from mpi4py cimport MPI
from mpi4py.mpi_c cimport *

cdef main():
    cdef MPI_Comm comm = MPI_COMM_WORLD

    cdef int size, rank
    MPI_Comm_size(comm, &size)
    MPI_Comm_rank(comm, &rank)

    cdef int N
    if rank == 0:
        N = <int>int(raw_input('Maximum number of terms?\n'))

    # broadcast input to other ranks <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    MPI_Bcast(&N, 1, MPI_INT, 0, comm)

    cdef unsigned int start_N = (rank*N    )//size
    cdef unsigned int end_N   = (rank*N + N)//size

    cdef unsigned int update_frequency = 1000000

    cdef double start_time
    if rank == 0:
        start_time = time()

    cdef double local_partial_sum = 0.0
    cdef double partial_sum

    cdef unsigned int i, j, counter = 1
    cdef double partial_result
    cdef double partial_error

    for i in xrange(start_N + 1, end_N + 1):
        local_partial_sum += (1.0/i)/i

        counter += 1

        if counter % update_frequency == 0:
            # parallel reduction of partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            MPI_Reduce(
                &local_partial_sum, &partial_sum,
                1, MPI_DOUBLE, MPI_SUM, 0,
                comm
            )

            if rank == 0:
                partial_result = sqrt(6*partial_sum)
                partial_error = fabs(pi - partial_result)
                print('partial error: %e' % partial_error)
                stdout.flush()

    # final parallel reduction of partial sum <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    MPI_Reduce(
        &local_partial_sum, &partial_sum,
        1, MPI_DOUBLE, MPI_SUM, 0,
        comm
    )

    cdef double stop_time
    cdef double elapsed_time
    if rank == 0:
        stop_time = time()
        elapsed_time = stop_time - start_time

        partial_result = sqrt(6*partial_sum)
        partial_error = fabs(pi - partial_result)

        print('\nPartial error after %d terms was %e' % (N, partial_error))
        print('Total time was %f seconds.\n' % elapsed_time)

if __name__ == '__main__':
    main()

