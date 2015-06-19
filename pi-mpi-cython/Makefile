
NUM_NODES:=4

include ../common.mk

build: pi_mpi_cython

pi_mpi_cython: pi_mpi_cython.o
	$(CC) $(LDFLAGS) $< -o $@ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

%.c: %.pyx
	$(CYTHON) $(CYTHON_FLAGS) $< -o $@

run: build
	@echo 100000000 | $(LAUNCHER) $(LAUNCHER_FLAGS) ./pi_mpi_cython

clean:
	rm -f pi_mpi_cython.c pi_mpi_cython.o pi_mpi_cython pi_mpi_cython.html

