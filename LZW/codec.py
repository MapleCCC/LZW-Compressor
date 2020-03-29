from typing import *

from .code_dict import CodeDict
from .iostream import FileInStreamer, write_to_file_from_stream
from .pep467 import getbyte
from .str_dict import StrDict

__all__ = ("encode_file", "decode_file", "lzw_encode", "lzw_decode")

# Char type is one-length byte object, like that in C language
Char = bytes
Code = int


def encode_file(filename: str, code_size: int) -> Iterable[int]:
    fs = FileInStreamer(filename, mode="rb")
    return lzw_encode(fs, code_size)


def decode_file(filename: str, codes: Iterable[Code], code_size: int) -> None:
    write_to_file_from_stream(lzw_decode(codes, code_size), filename, mode="wb")


def lzw_encode(text: Iterable[Char], code_size: int) -> Iterator[Code]:
    # The frequent operation is to find the longest prefix
    # substring in the code dict. If we use hash table,
    # we need to hash every intermediate string along the process,
    # which could be expensive.
    # TODO: Try trie data structure instead.

    code_dict = CodeDict(code_size)
    P = b""
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
    P = b""
    for code in codes:
        if code in str_dict:
            if P:
                str_dict.add_new_str(P + getbyte(str_dict[code], 0))
            P = str_dict[code]
            yield str_dict[code]
        else:
            str_dict.add_new_str(P + getbyte(P, 0))
            yield P + getbyte(P, 0)
            P = P + getbyte(P, 0)
