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
	pylint *.py **/*.py --disable=all --enable=W0611

reformat:
	isort *.py **/*.py
	black .

clean:
	rm -f lzw

.PHONY: all test clean
