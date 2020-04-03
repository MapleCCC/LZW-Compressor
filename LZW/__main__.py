#!/usr/bin/env python3

from itertools import chain
from typing import List

import click
from more_itertools import split_at

from .codec import LZWDecoder, LZWEncoder
from .extra_itertools import ijoin
from .lzwfile import (
    read_lzwfile_codes,
    read_lzwfile_header,
    write_lzwfile_codes,
    write_lzwfile_header,
)

# import fire
# import argparse


CODE_BIT: int = 12
VIRTUAL_EOF: int = 2 ** CODE_BIT - 1


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
    if len(files) == 0:
        raise ValueError("At least one file is needed to be compressed into archive")
    encoder = LZWEncoder(code_size=CODE_BIT)
    # TODO: Use more concise itertools, like more_itertools.interleave
    codes = chain(
        ijoin([VIRTUAL_EOF], (encoder.encode_file(file) for file in files)),
        [VIRTUAL_EOF],
    )
    write_lzwfile_header(archive, files)
    write_lzwfile_codes(archive, codes, code_size=CODE_BIT)


def _decompress(archive: str):
    filenames = read_lzwfile_header(archive)
    codes_list = split_at(
        read_lzwfile_codes(archive, code_size=CODE_BIT), lambda x: x == VIRTUAL_EOF
    )
    decoder = LZWDecoder(code_size=CODE_BIT)
    for filename, codes in zip(filenames, codes_list):
        decoder.decode_file(filename, codes)


if __name__ == "__main__":
    main()
