from itertools import chain
from typing import *

from code_dict import CodeDict
from iostream import FileInStreamer, write_to_file_from_stream
from str_dict import StrDict

Char = str
Code = int

# An encoding scheme that covers 0-255 ascii characters
extended_ascii_encoding = "utf-8"


def encode_file(filename: str, code_size: int) -> Iterable[int]:
    VIRTUAL_EOF = 2 ** code_size - 1
    fs = FileInStreamer(filename, encoding=extended_ascii_encoding, newline="")
    return chain(lzw_encode(fs, code_size), (VIRTUAL_EOF,))


def decode_file(filename: str, codes: Iterable[Code], code_size: int) -> None:
    write_to_file_from_stream(
        lzw_decode(codes, code_size),
        filename,
        encoding=extended_ascii_encoding,
        newline="",
    )


def lzw_encode(text: Iterable[Char], code_size: int) -> Iterator[Code]:
    # The frequent operation is to find the longest prefix
    # substring in the code dict. If we use hash table,
    # we need to hash every intermediate string along the process,
    # which could be expensive.
    # TODO: Try trie data structure instead.

    code_dict = CodeDict(code_size)
    P = ""
    for char in text:
        if P + char in code_dict:
            P = P + char
        else:
            yield code_dict[P]
            code_dict.add_new_code(P + char)
            P = char
    if P:
        yield code_dict[P]


def lzw_decode(codes: Iterable[Code], code_size: int) -> Iterator[Char]:
    str_dict = StrDict(code_size)
    P = ""
    for code in codes:
        if code in str_dict:
            if P:
                str_dict.add_new_str(P + str_dict[code][0])
            P = str_dict[code]
            yield str_dict[code]
        else:
            str_dict.add_new_str(P + P[0])
            yield P + P[0]
            P = P + P[0]
