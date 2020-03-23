#!/usr/bin/env python3

from ctypes import c_ulong
from pprint import PrettyPrinter
from typing import BinaryIO, Iterable, List

import click

# import fire
# import argparse

from code_dict import CodeDict
from str_dict import StrDict
from utils import *


# TODO: add unit test
# TODO: add feature supporting multiple input files
# TODO: consider rewriting in lazy evaluation / generator style, so as to save runtime space cost


print = PrettyPrinter().pprint

CODE_BIT: int = 12
VIRTUAL_EOF: int = 2 ** CODE_BIT - 1


def write_codes_to_file(fp: BinaryIO, codes: Iterable[int]) -> None:
    def write_code(f: BinaryIO, code: int, code_size: int):
        nonlocal buffer, buffer_load_bitsize

        if code_size > 24:
            raise ValueError("code_size should not be larger than 24 bits")

        offset = 32 - code_size - buffer_load_bitsize
        buffer = c_ulong(buffer.value | (code << offset))
        buffer_load_bitsize += code_size

        while buffer_load_bitsize >= 8:
            # FIXME
            code = buffer.value >> (32 - 8)
            f.write(bytes([code]))
            buffer = c_ulong(buffer.value << 8)
            buffer_load_bitsize -= 8

    buffer_load_bitsize = 0
    buffer = c_ulong(0)

    for code in codes:
        write_code(fp, code, CODE_BIT)
    # Padded with 0 to flush the leftover bits in the buffer
    write_code(fp, 0, 8)


def read_file_header(filename: str) -> Iterable[str]:
    with open(filename, "rb") as f:
        _filename = f.readline().strip()
        while _filename != b"":
            yield _filename.decode("ascii")
            _filename = f.readline().strip()


def write_file_header(fp: BinaryIO, filenames: Iterable[str]) -> None:
    for filename in filenames:
        fp.write(filename.encode("ascii") + b"\n")
    fp.write(b"\n")


def read_codes_from_file(filename: str) -> List[int]:
    def read_code(f: BinaryIO, code_size: int) -> int:
        nonlocal buffer, buffer_load_bitsize

        if code_size > 32:
            raise ValueError("code size should not be larger than 32 bits")

        while buffer_load_bitsize < code_size:
            offset = 32 - buffer_load_bitsize - 8
            byte = f.read(1)
            if not byte:
                raise RuntimeError("File abruptly ends before VIRTUAL_EOF is detected")
            buffer = c_ulong(buffer.value | (ord(byte) << offset))
            buffer_load_bitsize += 8

        code = buffer.value >> (32 - code_size)
        buffer = c_ulong(buffer.value << code_size)
        buffer_load_bitsize -= code_size
        return code

    codes: List[int] = []

    buffer = c_ulong(0)
    buffer_load_bitsize = 0

    with open(filename, "rb") as f:
        # Skip through file header
        filenames = []
        filename = f.readline().strip()
        while filename != b"":
            filenames.append(filename)
            filename = f.readline().strip()

        code = ""
        while code != VIRTUAL_EOF:
            code = read_code(f, CODE_BIT)
            codes.append(code)

        return codes


def lzw_encode(text: str) -> List[int]:
    # The frequent operation is to find the longest prefix
    # substring in the code dict. If we use hash table,
    # we need to hash every intermediate string along the process,
    # which could be expensive. Try trie data structure instead.
    encode_sequence: List[int] = []

    code_dict = CodeDict(code_bit=CODE_BIT)
    P = ""
    for char in text:
        if P + char in code_dict:
            P = P + char
        else:
            encode_sequence.append(code_dict[P])
            code_dict.add_new_code(P + char)
            P = char
    encode_sequence.append(code_dict[P])

    return encode_sequence


def encode_file(filename: str) -> Sequence[int]:
    with open(filename, "r", encoding="utf-8") as f:
        return lzw_encode(f.read()) + [VIRTUAL_EOF]


def lzw_decode(codes: List[int]) -> str:
    if len(codes) == 0:
        return ""

    decode_text = ""

    str_dict = StrDict(code_bit=CODE_BIT)
    code = codes[0]
    P = str_dict[code]
    decode_text += str_dict[code]
    for code in codes[1:]:
        if code == VIRTUAL_EOF:
            raise ValueError("Cannot decode EOF")
        if code in str_dict:
            str_dict.add_new_str(P + str_dict[code][0])
            P = str_dict[code]
            decode_text += str_dict[code]
        else:
            str_dict.add_new_str(P + P[0])
            decode_text += P + P[0]
            P = P + P[0]

    return decode_text


@click.group()
def main():
    pass


@main.command()
@click.argument("archive")
@click.argument("files", nargs=-1)
def compress(archive: str, files: List[str]):
    if len(files) == 0:
        raise ValueError("At least one file is needed to be compressed into archive")
    codes = itertools.chain.from_iterable(encode_file(file) for file in files)
    with open(archive, "wb") as f:
        write_file_header(f, files)
        write_codes_to_file(f, codes)


@main.command()
@click.argument("archive")
def decompress(archive: str):
    filenames = list(read_file_header(archive))
    codes_list = list(isplit(read_codes_from_file(archive), VIRTUAL_EOF))
    assert len(filenames) == len(codes_list)
    for i, codes in enumerate(codes_list):
        write_file_content(filenames[i], lzw_decode(codes))


if __name__ == "__main__":
    main()
