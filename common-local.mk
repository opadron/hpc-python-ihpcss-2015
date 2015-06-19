
PYTHON:=python2

CYTHON:=cython
CYTHON_FLAGS:=-2 -a --embed=main

CC:=gcc
CFLAGS:=-O3 -I/usr/include/python2.7
LDFLAGS:=
LIBS:=-lm -lpython2.7

LAUNCHER:=
LAUNCHER_FLAGS:=

all: build

