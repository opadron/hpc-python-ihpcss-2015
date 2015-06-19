
from libc.stdlib cimport malloc, free
from libc.math cimport fabs, fmax
from libc.stdio cimport printf, scanf, fflush, FILE

cdef FILE *STDOUT = NULL

#TODO(opadron) consider using struct timespec
from time import time

def main():
    cdef unsigned int COLUMNS    =              1000
    cdef unsigned int COLUMNS_P1 = COLUMNS    +    1
    cdef unsigned int COLUMNS_P2 = COLUMNS_P1 +    1

    cdef unsigned int ROWS       =              1000
    cdef unsigned int ROWS_P1    = ROWS       +    1
    cdef unsigned int ROWS_P2    = ROWS_P1    +    1

    cdef unsigned int NUM_ELEMENTS = COLUMNS_P2*ROWS_P2

    cdef unsigned int row_offset;
    cdef unsigned int top_row_offset;
    cdef unsigned int bottom_row_offset;

    cdef unsigned int i, j

    cdef double MAX_TEMP_ERROR = 0.01
    cdef double dt = 1.1*MAX_TEMP_ERROR

    cdef unsigned int max_iterations
    printf('Maximum iterations [100-4000]?\n')
    scanf('%u', &max_iterations)

    cdef unsigned int iteration = 1

    cdef double start_time = <double>time()

    # initialize
    cdef double *Temperature = <double *>malloc(
        NUM_ELEMENTS*sizeof(double)
    )

    cdef double *Temperature_last = <double *>malloc(
        NUM_ELEMENTS*sizeof(double)
    )

    row_offset = 0
    for i in range(0, ROWS_P1):
        for j in range(0, COLUMNS_P1):
            Temperature_last[row_offset + j] = 0.0

    row_offset = COLUMNS_P2
    for i in range(1, ROWS_P1):
        Temperature_last[row_offset - 1] = (100.0/ROWS)*i
        row_offset += COLUMNS_P2

    row_offset -= COLUMNS_P2 + COLUMNS_P2
    for j in range(1, COLUMNS_P2):
        Temperature_last[row_offset + j] = (100.0/COLUMNS)*j

    # do until error is minimal or until max steps
    while dt > MAX_TEMP_ERROR and iteration <= max_iterations:
        dt = 0.0
        # main calculation: average my four neighbors

        top_row_offset    =                           0
        row_offset        = top_row_offset + COLUMNS_P2
        bottom_row_offset = row_offset     + COLUMNS_P2

        for i in xrange(1, ROWS_P1):
            for j in xrange(1, COLUMNS_P1):
                Temperature[row_offset + j] = 0.25*(
                    Temperature_last[top_row_offset    + j    ] +
                    Temperature_last[bottom_row_offset + j    ] +
                    Temperature_last[row_offset        + j + 1] +
                    Temperature_last[row_offset        + j - 1]
                )

                dt = fmax(dt, fabs(
                    Temperature[row_offset + j] -
                    Temperature_last[row_offset + j]
                ))

            top_row_offset    += COLUMNS_P2
            row_offset        += COLUMNS_P2
            bottom_row_offset += COLUMNS_P2

        # copy grid to old grid for next iteration
        row_offset = COLUMNS_P2
        for i in range(1, ROWS_P1):
            for j in range(1, COLUMNS_P1):
                Temperature_last[row_offset + j] =  (
                    Temperature[row_offset + j]
                )
            row_offset += COLUMNS_P2

        # periodically print test values
        if iteration % 100 == 0:
            # track progress
            printf(
                '---------- Iteration number: %d ------------\n',
                iteration
            )

            row_offset = (ROWS - 5)*COLUMNS_P2
            for i in range(ROWS - 5, ROWS + 1):
                printf(
                    '[%d,%d]: %5.2f  ',
                    i, i, Temperature[row_offset + j]
                )

            printf('\n')
            fflush(STDOUT)

        iteration += 1

    cdef double stop_time, elapsed_time
    stop_time = <double>time()
    elapsed_time = stop_time - start_time

    printf(
        '\nMax error at iteration %d was %f\n',
        iteration - 1, dt
    )
    printf('Total time was %f seconds.\n\n', elapsed_time)

    free(Temperature)
    free(Temperature_last)

if __name__ == '__main__':
    main()

