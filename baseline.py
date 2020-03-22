#!/usr/bin/env python3

from ctypes import c_ulong
from typing import BinaryIO, List, Sequence, Dict
import click
import fire
from pprint import PrettyPrinter

print = PrettyPrinter().pprint

from code_dict import CodeDict
from str_dict import StrDict


# TODO: add unit test
# TODO: add feature supporting multiple input files

CODE_BIT: int = 12
VIRTUAL_EOF: int = 2 ** CODE_BIT - 1


def write_codes_to_file(filename: str, codes: Sequence[int]) -> None:
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

    with open(filename, "wb") as f:
        # FIXME
        f.write(b"Ephesians_.txt" + b"\n\n")
        for code in codes:
            write_code(f, code, CODE_BIT)
        write_code(f, VIRTUAL_EOF, CODE_BIT)
        write_code(f, 0, 8)


def read_codes_from_file(filename: str) -> List[int]:
    def read_code(f: BinaryIO, code_size: int) -> int:
        nonlocal buffer, buffer_load_bitsize

        while buffer_load_bitsize < code_size:
            offset = 32 - buffer_load_bitsize - 8
            buffer = c_ulong(buffer.value | (ord(f.read(1)) << offset))
            buffer_load_bitsize += 8

        code = buffer.value >> (32 - code_size)
        buffer = c_ulong(buffer.value << code_size)
        buffer_load_bitsize -= code_size
        return code

    codes: List[int] = []

    buffer = c_ulong(0)
    buffer_load_bitsize = 0

    with open(filename, "rb") as f:
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

    # print(sorted(code_dict._storage.items(), key=lambda x: x[1]))

    return encode_sequence


def lzw_decode(codes: List[int]) -> str:
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


# @click.command()
# @click.option("-o", "lzw_filename", default="baseline_output", help="lzw_filenames")
# @click.argument("input_filename")
def main(lzw_filename, input_filename):
    with open(input_filename, "r", encoding="utf-8") as f:
        content = f.read()

    encode_sequence = lzw_encode(content)
    write_codes_to_file(lzw_filename, encode_sequence)


# if __name__ == "__main__":
#     fire.Fire(main)
# main()
