CC=gcc
CFLAGS=-g
PROGS=lzw

all: ${PROGS}

lzw: lzw.c

test:
	pytest test --hypothesis-show-statistics

simple-test:
	pytest test

lint:
	pylint *.py **/*.py --errors-only

check-unused-import:
	pylint **/*.py --disable=all --enable=W0611

clean:
	rm -f lzw

.PHONY: all test clean
