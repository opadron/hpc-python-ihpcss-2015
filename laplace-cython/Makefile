
NUM_NODES:=1

include ../common.mk

export OMP_NUM_THREADS:=16

build: laplace_cython

laplace_cython: laplace_cython.o
	$(CC) $(LDFLAGS) $< -o $@ $(LIBS)

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

%.c: %.pyx
	$(CYTHON) $(CYTHON_FLAGS) $< -o $@

run: build
	@export OMP_NUM_THREADS=$(OMP_NUM_THREADS) ; \
	echo 3400 | $(LAUNCHER) $(LAUNCHER_FLAGS) ./laplace_cython

clean:
	rm -f laplace_cython.c    \
	      laplace_cython.o    \
	      laplace_cython.html \
	      laplace_cython

