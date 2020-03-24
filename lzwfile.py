"""
LZW format is an archive and compression standard. This module
provides simple tools to retrieve and process LZW files.
"""

import os
from ctypes import c_ulong
from itertools import chain
from typing import *

from iostream import FileInStreamer

Entry = str
Header = Iterable[Entry]
Code = int


def read_lzwfile_header(lzwfile: str) -> Iterable[str]:
    # From doc, note following behavior,
    # BinaryIO.readline() treat b"\n" as terminate
    # bytes.strip() treat ASCII whitespace characters (including b"\r", b"\n") as to be removed
    with open(lzwfile, "rb") as f:
        entry = f.readline().strip()
        while entry != b"":
            yield entry.decode("ascii")
            entry = f.readline().strip()


def write_lzwfile_header(lzwfile: str, header: Header) -> None:
    if os.path.isfile(lzwfile):
        # TODO: how to implement?
        raise NotImplementedError
    else:
        with open(lzwfile, "rb") as f:
            for entry in header:
                f.write((entry + os.linesep).encode("ascii"))
            f.write(os.linesep.encode("ascii"))


def read_lzwfile_codes(lzwfile: str, code_size: int) -> Iterator[Code]:
    fs = FileInStreamer(lzwfile, "rb")

    # Skip through the header
    past = ppast = pppast = b""
    for i, byte in enumerate(fs):
        if i == 0 and byte == b"\n":
            # The lzwfile has empty header
            return
        if past + byte == b"\n\n" or pppast + ppast + past + byte == b"\r\n\r\n":
            break
        else:
            pppast = ppast
            ppast = past
            past = byte

    if code_size > 32:
        raise ValueError("code size should not be larger than 32 bits")

    buffer = c_ulong(0)
    buffer_load_bitsize = 0

    for byte in fs:
        offset = 32 - buffer_load_bitsize - 8
        buffer = c_ulong(buffer.value | (ord(byte) << offset))
        buffer_load_bitsize += 8

        if buffer_load_bitsize >= code_size:
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

        # Padded with 0 to flush the leftover bits in the buffer
        padded = chain(codes, (0,))

        for code in padded:
            offset = 32 - code_size - buffer_load_bitsize
            buffer = c_ulong(buffer.value | (code << offset))
            buffer_load_bitsize += code_size

            while buffer_load_bitsize >= 8:
                code = buffer.value >> (32 - 8)
                f.write(bytes([code]))
                buffer = c_ulong(buffer.value << 8)
                buffer_load_bitsize -= 8

    if os.path.isfile(lzwfile):
        with open(lzwfile, "rb+") as f:
            # Skip through the header
            _filename = f.readline().strip()
            while _filename != b"":
                yield _filename.decode("ascii")
                _filename = f.readline().strip()

            f.truncate()
            _write_codes(f)
    else:
        with open(lzwfile, "wb") as f:
            f.write(b"\n")
            _write_codes(f)
