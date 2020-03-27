# MAKEFLAGS += .silent

CXX=g++
CXXFLAGS=-g
PROGS=lzw

all: ${PROGS}

lzw: lzw.cpp

test:
	pytest test/

test-stat:
	pytest test/ --hypothesis-show-statistics

test-cov:
	pytest --cov=LZW test/
	coverage html

lint:
	pylint *.py **/*.py --errors-only

check-unused-imports:
	pylint *.py **/*.py --disable=all --enable=W0611

reformat:
	isort *.py **/*.py
	black .

clean:
	rm -f lzw

.PHONY: all test simple-test lint check-unused-imports reformat clean
