#!/usr/bin/env python3

from itertools import chain
from typing import List

import click
from more_itertools import split_after

from .codec import LZWDecoder, LZWEncoder
from .lzwfile import (
    read_lzwfile_codes,
    read_lzwfile_header,
    write_lzwfile_codes,
    write_lzwfile_header,
)

# import fire
# import argparse


CODE_BITSIZE: int = 12
VIRTUAL_EOF: int = 2 ** CODE_BITSIZE - 1


@click.group()
def main():
    pass


@main.command()
@click.option("-o", "--output", "archive", default="a.lzw")
@click.argument("files", nargs=-1)
def compress(archive: str, files: List[str]):
    _compress(archive, files)


@main.command()
@click.argument("archive")
def decompress(archive: str):
    _decompress(archive)


def _compress(archive: str, files: List[str]):
    if not files:
        raise ValueError("At least one file is needed to be compressed into archive")

    write_lzwfile_header(archive, files)

    encoder = LZWEncoder(CODE_BITSIZE)
    codes = chain.from_iterable(encoder.encode_file(file) for file in files)
    write_lzwfile_codes(archive, codes, CODE_BITSIZE)


def _decompress(archive: str):
    filenames = read_lzwfile_header(archive)
    codes_list = split_after(
        read_lzwfile_codes(archive, CODE_BITSIZE), lambda x: x == VIRTUAL_EOF
    )
    decoder = LZWDecoder(CODE_BITSIZE)
    for filename, codes in zip(filenames, codes_list):
        decoder.decode_file(filename, codes)


if __name__ == "__main__":
    main()
