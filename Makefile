# MAKEFLAGS += .silent

test:
	pytest test/

test-stat:
	pytest test/ --hypothesis-show-statistics

test-cov:
	pytest --cov=LZW test/
	coverage html

lint:
	# For pylint, "lint all files under all subdir" is a long requested feature that is not yet realized
	# Ref: https://github.com/PyCQA/pylint/issues/352
	find LZW/ test/ -type f -name "*.py" | xargs pylint

check-unused-imports:
	# For pylint, "lint all files under all subdir" is a long requested feature that is not yet realized
	# Ref: https://github.com/PyCQA/pylint/issues/352
	find LZW/ test/ -type f -name "*.py" | xargs pylint --disable=all --enable=W0611

# Set alias for easy typing
cui: check-unused-imports

reformat:
	# executing "isort ." command yields failure, why? TODO: try to deal with it.
	find LZW/ test/ -type f -name "*.py" | xargs isort
	black .

# TODO: recursively remove pycache folders
clean:
	rm -rf __pycache__/ .pytest_cache/ .hypothesis/ htmlcov/ .coverage
	# py3clean script

.PHONY: test test-stat test-cov lint check-unused-imports reformat clean
