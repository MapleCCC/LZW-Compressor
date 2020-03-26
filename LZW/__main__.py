#!/usr/bin/env python3

from typing import List

import click

from .codec import decode_file, encode_file
from .extra_itertools import ijoin, isplit
from .lzwfile import (
    read_lzwfile_codes,
    read_lzwfile_header,
    write_lzwfile_codes,
    write_lzwfile_header,
)

# import fire
# import argparse


# TODO: add unit test
# TODO: consider rewriting in lazy evaluation / generator style, so as to save runtime space cost
# Another importance of writing in stream style is that so our script can handle input that is infinitely large
# TODO: handle the corner case of zero file is input for compression
# TODO: handle the corner case of empty file
# TODO: why is our encode output different with the example one?
# TODO: preserve newline format. Disable Python's builtin default universal newline support feature.
# TODO: ask for clarification of spec: should we handle the case of zero compressed file?


CODE_BIT: int = 12
VIRTUAL_EOF: int = 2 ** CODE_BIT - 1


@click.group()
def main():
    pass


@main.command()
@click.argument("archive")
@click.argument("files", nargs=-1)
def compress(archive: str, files: List[str]):
    if len(files) == 0:
        raise ValueError("At least one file is needed to be compressed into archive")
    codes = ijoin(
        [VIRTUAL_EOF], (encode_file(file, code_size=CODE_BIT) for file in files)
    )
    write_lzwfile_header(archive, files)
    write_lzwfile_codes(archive, codes, code_size=CODE_BIT)


@main.command()
@click.argument("archive")
def decompress(archive: str):
    filenames = read_lzwfile_header(archive)
    codes_list = isplit(read_lzwfile_codes(archive, code_size=CODE_BIT), VIRTUAL_EOF)
    for filename, codes in zip(filenames, codes_list):
        decode_file(filename, codes, code_size=CODE_BIT)


if __name__ == "__main__":
    main()
