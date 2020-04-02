# LZW Compressor

## Introduction

LZW is an archive format that utilize power of LZW compression algorithm. LZW compression algorithm is a dictionary-based loseless algorithm. It's a old algorithm suitable for beginner to practice.

## Installation

Prerequisites: Git, pip.

```bash
$ git clone https://github.com/MapleCCC/LZW-Compressor.git

$ cd LZW-Compressor

# Install in editable mode
$ pip install -e .  # Note the dot
```

## Usage

```bash
# Compression
$ lzw compress [-o|--output <ARCHIVE>] <FILES>...

# Decompression
$ lzw decompress <ARCHIVE>
```

## License

[WTFPL 2.0](./LICENSE)

<a href="http://www.wtfpl.net/"><img src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png" width="80" height="15" alt="WTFPL" /></a>

Except those that are done by CUHK CSCI3280 2020 Spring teaching team, whose work is in the first commit.
