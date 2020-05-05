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

        prefix = b""
        for char in text:
            current_word = prefix + char
            if current_word in self._code_dict:
                prefix = current_word
            else:
                yield self._code_dict[prefix]
                self._code_dict.add_new_code(current_word)
                prefix = char
        if prefix:
            yield self._code_dict[prefix]


class LZWDecoder:
    def __init__(self, code_size: int) -> None:
        self._str_dict: StrDict = StrDict(code_size)
        self._virtual_eof = 2 ** code_size - 1

    __slots__ = ["_str_dict", "_virtual_eof"]

    def decode_file(self, filename: AnyStr, codes: Iterable[Code]) -> None:
        write_to_file_from_stream(self._decode(codes), filename, mode="wb")

    def _decode(self, codes: Iterable[Code]) -> Iterator[bytes]:
        prefix = b""
        for code in codes:
            if code == self._virtual_eof:
                break
            if code in self._str_dict:
                if prefix:
                    current_word = prefix + getbyte(self._str_dict[code], 0)
                    self._str_dict.add_new_str(current_word)
                prefix = self._str_dict[code]
                yield self._str_dict[code]
            else:
                current_word = prefix + getbyte(prefix, 0)
                self._str_dict.add_new_str(current_word)
                yield current_word
                prefix = current_word
