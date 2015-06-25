
PYTHON:=python2

ANACONDA_HOME:=/opt/anaconda

SITE_PACKAGES:=/opt/anaconda/lib/python2.7/site-packages
NUMPY_INCLUDE:=$(SITE_PACKAGES)/numpy/core/include

CYTHON:=cython
CYTHON_FLAGS:=-2 --embed=main -a
CYTHON_FLAGS:=$(CYTHON_FLAGS) -I$(SITE_PACKAGES) -I$(SITE_PACKAGES)/mpi4py/include

CC:=mpicc
CFLAGS:=-O3 -I$(ANACONDA_HOME)/include/python2.7
CFLAGS:=$(CFLAGS) -I$(NUMPY_INCLUDE)

LDFLAGS:=-L$(ANACONDA_HOME)/lib
LIBS:=-lm -lpython2.7

export OMP_NUM_THREADS:=16

LAUNCHER:=mpirun
LAUNCHER_FLAGS:=-n $(NUM_NODES) -f ../hostfile

all: build

