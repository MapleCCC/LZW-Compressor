CC=gcc
CFLAGS=-g
PROGS=lzw

all: ${PROGS}

lzw: lzw.c

test:
	pytest test

clean:
	rm -f lzw

.PHONY: all test clean
