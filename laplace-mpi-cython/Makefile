
NUM_NODES:=4

include ../common.mk

export OMP_NUM_THREADS:=16

build: laplace_mpi_cython

laplace_mpi_cython: laplace_mpi_cython.o
	$(CC) $(LDFLAGS) $< -o $@ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

%.c: %.pyx
	$(CYTHON) $(CYTHON_FLAGS) $< -o $@

run: build
	@export OMP_NUM_THREADS=$(OMP_NUM_THREADS) ; \
	echo 3400 | $(LAUNCHER) $(LAUNCHER_FLAGS) ./laplace_mpi_cython

clean:
	rm -f laplace_mpi_cython.c    \
	      laplace_mpi_cython.o    \
	      laplace_mpi_cython.html \
	      laplace_mpi_cython

