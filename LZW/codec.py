from typing import AnyStr, Iterable, Iterator

from .code_dict import CodeDict
from .extra_itertools import iappend
from .iostream import FileInStreamer, write_to_file_from_stream
from .pep467 import getbyte
from .str_dict import StrDict

__all__ = ("LZWEncoder", "LZWDecoder")

# Char type is one-length byte object, like that in C language
Char = bytes
Code = int


class LZWEncoder:
    def __init__(self, code_size: int) -> None:
        self._code_dict = CodeDict(code_size)
        self._virtual_eof = 2 ** code_size - 1

    __slots__ = ["_code_dict", "_virtual_eof"]

    def encode_file(self, filename: AnyStr) -> Iterable[Code]:
        fs = FileInStreamer(filename, mode="rb")
        return iappend(self._encode(fs), self._virtual_eof)

    def _encode(self, text: Iterable[Char]) -> Iterator[Code]:
        # The frequent operation is to find the longest prefix
        # substring in the code dict. If we use hash table,
        # we need to hash every intermediate string along the process,
        # which could be expensive.
        # TODO: Try trie data structure instead.

        P = b""
        for char in text:
            if P + char in self._code_dict:
                P = P + char
            else:
                yield self._code_dict[P]
                self._code_dict.add_new_code(P + char)
                P = char
        if P:
            yield self._code_dict[P]


class LZWDecoder:
    def __init__(self, code_size: int) -> None:
        self._str_dict: StrDict = StrDict(code_size)
        self._virtual_eof = 2 ** code_size - 1

    __slots__ = ["_str_dict", "_virtual_eof"]

    def decode_file(self, filename: AnyStr, codes: Iterable[Code]) -> None:
        write_to_file_from_stream(self._decode(codes), filename, mode="wb")

    def _decode(self, codes: Iterable[Code]) -> Iterator[Char]:
        P = b""
        for code in codes:
            if code == self._virtual_eof:
                break
            if code in self._str_dict:
                if P:
                    self._str_dict.add_new_str(P + getbyte(self._str_dict[code], 0))
                P = self._str_dict[code]
                yield self._str_dict[code]
            else:
                self._str_dict.add_new_str(P + getbyte(P, 0))
                yield P + getbyte(P, 0)
                P = P + getbyte(P, 0)
