# MAKEFLAGS += .silent

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

# Set alias for easy typing
cui: check-unused-imports

reformat:
	isort *.py **/*.py
	black .

# TODO: recursively remove pycache folders
clean:
	rm -rf __pycache__/ .pytest_cache/ .hypothesis/ htmlcov/ .coverage
	# py3clean script

.PHONY: test test-stat test-cov lint check-unused-imports reformat clean
