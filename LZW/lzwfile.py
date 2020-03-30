"""
LZW format is an archive and compression standard. This module
provides simple tools to retrieve and process LZW files.
"""

import os
from itertools import takewhile
from typing import *

# non-wildcard import, because BinaryIO is not part of public API
from typing import BinaryIO

from .bitarray import Bitarray
from .iostream import FileInStreamer

__all__ = (
    "read_lzwfile_header",
    "read_lzwfile_codes",
    "write_lzwfile_header",
    "write_lzwfile_codes",
)

Entry = str
Header = Iterable[Entry]
Code = int


def read_lzwfile_header(lzwfile: str) -> Iterable[str]:
    with open(lzwfile, "rb") as f:
        entry = f.readline().strip()
        while entry != b"":
            yield entry.decode()
            entry = f.readline().strip()


def write_lzwfile_header(lzwfile: str, header: Header) -> None:
    if os.path.isfile(lzwfile):
        # TODO: how to implement?
        raise NotImplementedError
    else:
        with open(lzwfile, "wb") as f:
            for entry in header:
                f.write(entry.encode() + b"\n")
            f.write(b"\n")


def read_lzwfile_codes(lzwfile: str, code_size: int) -> Iterator[Code]:
    def readline_from_bytestream(fs: FileInStreamer) -> bytes:
        return b"".join(takewhile(lambda byte: byte != b"\n", fs))

    fs = FileInStreamer(lzwfile, "rb")

    # Skip through the header
    line = readline_from_bytestream(fs)
    while line:
        line = readline_from_bytestream(fs)

    buffer = Bitarray()

    for byte in fs:
        print(f"read in byte: {byte}")
        buffer.push_bytes_back(byte)

        print(f"Length of bitarray: {len(buffer)}")

        while len(buffer) >= code_size:
            code = buffer[:code_size].to_int()
            buffer = buffer[code_size:]
            print(f"yield one code: {code}")
            yield code


def write_lzwfile_codes(lzwfile, codes: Iterable[Code], code_size: int) -> None:
    def _write_codes(f: BinaryIO):
        buffer = Bitarray()

        for code in codes:
            buffer += Bitarray.from_int(code, code_size)

            while len(buffer) >= 8:
                byte = buffer.pop_byte_front()
                print(f"Write out byte: {byte}")
                f.write(byte)

        # padded with 0, and flush out the left bits
        # because LZW code bit size must be larger than 8-bit
        # so no need to worry that the padded zeros would be
        # mistreated as extra code.
        if len(buffer) > 0:
            buffer.push_bytes_back(b"\x00")
            byte = buffer.pop_byte_front()
            f.write(byte)

    if os.path.isfile(lzwfile):
        with open(lzwfile, "rb+") as f:
            # Skip through the header
            _filename = f.readline().strip()
            while _filename != b"":
                _filename = f.readline().strip()

            f.truncate()
            _write_codes(f)  # type: ignore
    else:
        with open(lzwfile, "wb") as f:
            f.write(b"\n")
            _write_codes(f)  # type: ignore
