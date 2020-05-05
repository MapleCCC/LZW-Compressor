MAKEFLAGS += .silent

TEST_DIR=tests
SRC_DIR=LZW

test:
	pytest ${TEST_DIR}

test-stat:
	pytest ${TEST_DIR} --hypothesis-show-statistics

test-cov:
	pytest --cov=${SRC_DIR} ${TEST_DIR}
	# Alternatively, we can run: coverage run
	coverage html
	# TODO: possibly also open index.html in browser
	python -m webbrowser -n htmlcov/index.html

lint:
	# cd ${SRC_DIR} && pylint_runner rc
	# cd ${TEST_DIR} && pylint_runner rc
	# For pylint, "lint all files under all subdir" is a long requested feature that is not yet realized
	# Ref: https://github.com/PyCQA/pylint/issues/352
	find ${SRC_DIR} ${TEST_DIR} -type f -name "*.py" | xargs pylint

check-unused-imports:
	# For pylint, "lint all files under all subdir" is a long requested feature that is not yet realized
	# Ref: https://github.com/PyCQA/pylint/issues/352
	find ${SRC_DIR} ${TEST_DIR} -type f -name "*.py" | xargs pylint --disable=all --enable=W0611

# Set alias for easy typing
cui: check-unused-imports

todo:
	grep -ri --include=*.py TODO

reformat:
	# executing "isort ." command yields failure, why? TODO: try to deal with it.
	find ${SRC_DIR} ${TEST_DIR} -type f -name "*.py" | xargs isort
	black .

# TODO: recursively remove pycache folders
clean:
	rm -rf __pycache__/ .pytest_cache/ .hypothesis/ htmlcov/ .coverage
	# py3clean script

.PHONY: test test-stat test-cov lint check-unused-imports cui todo reformat clean
