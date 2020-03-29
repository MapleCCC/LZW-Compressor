"""
LZW format is an archive and compression standard. This module
provides simple tools to retrieve and process LZW files.
"""

import os
from ctypes import c_ulong
from itertools import takewhile
from typing import *

# non-wildcard import, because BinaryIO is not part of public API
from typing import BinaryIO

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

extended_ascii_encoding = "utf-8"


def read_lzwfile_header(lzwfile: str) -> Iterable[str]:
    # From doc, note following behavior,
    # BinaryIO.readline() treat b"\n" as terminate
    # bytes.strip() treat ASCII whitespace characters (including b"\r", b"\n") as to be removed
    with open(lzwfile, "rb") as f:
        entry = f.readline().strip()
        while entry != b"":
            yield entry.decode(extended_ascii_encoding)
            entry = f.readline().strip()


def write_lzwfile_header(lzwfile: str, header: Header) -> None:
    if os.path.isfile(lzwfile):
        # TODO: how to implement?
        raise NotImplementedError
    else:
        with open(lzwfile, "wb") as f:
            for entry in header:
                f.write((entry + os.linesep).encode(extended_ascii_encoding))
            f.write(os.linesep.encode(extended_ascii_encoding))


def read_lzwfile_codes(lzwfile: str, code_size: int) -> Iterator[Code]:
    def readline_from_bytestream(fs: FileInStreamer) -> bytes:
        # ret = b""
        # for byte in fs:
        #     ret += byte
        #     if byte == b"\n":
        #         break
        # return ret
        return b"".join(takewhile(lambda byte: byte != b"\n", fs))

    fs = FileInStreamer(lzwfile, "rb")

    # Skip through the header
    line = readline_from_bytestream(fs).strip()
    while line:
        line = readline_from_bytestream(fs).strip()

    if code_size > 32:
        raise ValueError("code size should not be larger than 32 bits")

    buffer = c_ulong(0)
    buffer_load_bitsize = 0

    for byte in fs:
        offset = 32 - buffer_load_bitsize - 8
        buffer = c_ulong(buffer.value | (ord(byte) << offset))
        buffer_load_bitsize += 8

        while buffer_load_bitsize >= code_size:
            code = buffer.value >> (32 - code_size)
            buffer = c_ulong(buffer.value << code_size)
            buffer_load_bitsize -= code_size
            yield code


def write_lzwfile_codes(lzwfile, codes: Iterable[Code], code_size: int) -> None:
    def _write_codes(f: BinaryIO):
        buffer_load_bitsize = 0
        buffer = c_ulong(0)

        max_code_size = 32 - 8
        if code_size > max_code_size:
            raise ValueError(
                f"code_size should not be larger than {max_code_size} bits"
            )

        for code in codes:
            offset = 32 - code_size - buffer_load_bitsize
            buffer = c_ulong(buffer.value | (code << offset))
            buffer_load_bitsize += code_size

            while buffer_load_bitsize >= 8:
                byte = buffer.value >> (32 - 8)
                f.write(str(byte).encode("ascii"))
                buffer = c_ulong(buffer.value << 8)
                buffer_load_bitsize -= 8

        # TODO: deal with the case that code_size is less than 4
        # padded with 0, and flush out the left bits
        if buffer_load_bitsize > 0:
            byte = buffer.value >> (32 - 8)
            f.write(str(byte).encode("ascii"))

    if os.path.isfile(lzwfile):
        with open(lzwfile, "rb+") as f:
            # Skip through the header
            _filename = f.readline().strip()
            while _filename != b"":
                _filename = f.readline().strip()

            f.truncate()
            _write_codes(f)
    else:
        with open(lzwfile, "wb") as f:
            f.write(os.linesep.encode(extended_ascii_encoding))
            _write_codes(f)
