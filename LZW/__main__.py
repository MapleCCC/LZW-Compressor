#!/usr/bin/env python3

import os
from itertools import chain
from typing import List

import click
from more_itertools import split_after

from .codec import LZWDecoder, LZWEncoder
from .config import CODE_BITSIZE, VIRTUAL_EOF
from .lzwfile import (
    read_lzwfile_codes,
    read_lzwfile_header,
    write_lzwfile_codes,
    write_lzwfile_header,
)

# import fire
# import argparse


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("-o", "--output", "archive", default="a.lzw")
@click.argument("files", nargs=-1)
def compress(archive: str, files: List[str]) -> None:
    lzw_compress(archive, files)


@main.command()
@click.argument("archive")
def decompress(archive: str) -> None:
    lzw_decompress(archive)


def lzw_compress(archive: str, files: List[str]) -> None:
    if not files:
        raise ValueError("At least one file is needed to be compressed into archive")

    # Here is a surprising bug: if (archive in files) == True, then even if archive is
    # originally non-existent, no exception is raised. This is due to lazy evaluation.
    # One solution to this is to test file existence at the very first beginning, and fail early,
    # to prevent surprising errors later on.
    if not all(map(os.path.isfile, files)):
        # FIXME
        raise FileNotFoundError(f"Some files are non-existent: {files}")

    write_lzwfile_header(archive, files)

    encoder = LZWEncoder(CODE_BITSIZE)
    codes = chain.from_iterable(encoder.encode_file(file) for file in files)
    write_lzwfile_codes(archive, codes, CODE_BITSIZE)


def lzw_decompress(archive: str) -> None:
    filenames = read_lzwfile_header(archive)
    codes_list = split_after(
        read_lzwfile_codes(archive, CODE_BITSIZE), lambda x: x == VIRTUAL_EOF
    )
    decoder = LZWDecoder(CODE_BITSIZE)
    for filename, codes in zip(filenames, codes_list):
        decoder.decode_file(filename, codes)


if __name__ == "__main__":
    main()
