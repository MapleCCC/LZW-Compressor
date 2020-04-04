# LZW Compressor

[![License](https://img.shields.io/github/license/MapleCCC/LZW-Compressor?color=00BFFF)](http://www.wtfpl.net/)
[![travisci](https://www.travis-ci.com/MapleCCC/LZW-Compressor.svg?branch=master)](https://travis-ci.com/MapleCCC/LZW-Compressor)
[![codecov](https://codecov.io/gh/MapleCCC/LZW-Compressor/branch/master/graph/badge.svg)](https://codecov.io/gh/MapleCCC/LZW-Compressor)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- [![Build Status](https://img.shields.io/travis/MapleCCC/LZW-Compressor.svg?logo=travis)](https://travis-ci.com/MapleCCC/LZW-Compressor) -->
<!-- [![Test Coverage](https://img.shields.io/codecov/c/github/MapleCCC/LZW-Compressor/master?logo=codecov)](https://codecov.io/gh/MapleCCC/LZW-Compressor) -->

## Introduction

LZW is an archive format that utilize power of LZW compression algorithm. [LZW compression algorithm](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) is a dictionary-based loseless algorithm. It's an old algorithm suitable for beginner to practice.

Internal algorithm processes byte data. So it's applicable to any file types, besides text file. Although it may not be able to achieve substantial compression rate for some file types that are already compressed efficiently, such as PDF files.

## Installation

Prerequisites: Python>=3.6, [Git](https://git-scm.com/), [pip](https://pip.pypa.io/en/stable/).

```bash
$ git clone https://github.com/MapleCCC/LZW-Compressor.git

$ cd LZW-Compressor

# You can optionally create a virtual environment for isolation purpose
$ python -m virtualenv .venv
$ source .venv/Scripts/activate

# Install requirements
$ python -m pip install -r requirements.txt

# Install in editable mode
$ python -m pip install -e .  # Mind the dot at the end
```

## Usage

Use as command line tool:

```bash
# Compression
$ lzw compress [-o|--output <ARCHIVE>] <FILES>...

# Decompression
$ lzw decompress <ARCHIVE>
```

Use as module:

```python
from LZW import lzw_compress, lzw_decompress

lzw_compress("a.lzw", "file1", "file2")
lzw_decompress("a.lzw")
```

## Test

The project uses pytest and hypothesis as test framework. Property-based testing is adopted for flexibility and conciseness.

```bash
# Install test requirements
$ python -m pip install -r requirements-test.txt

# Base test
$ make test

# Test coverage
$ make test-cov
```

## Benchmark

[...]

## License

[WTFPL 2.0](./LICENSE)

[![WTFPL](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-1.png)](http://www.wtfpl.net/)
<!-- <a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a> -->

Except those that are done by CUHK CSCI3280 2020 Spring teaching team, whose work is in the first commit.
