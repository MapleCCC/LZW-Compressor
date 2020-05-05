from typing import Dict

from .trie import Trie
from .utils import ascii2byte


class StrDict:
    def __init__(self, code_bitsize: int) -> None:
        if code_bitsize <= 8:
            raise ValueError("Code bit size should be larger than 8")

        self._storage: Dict[int, bytes] = Trie()
        # The first 256 codes are reserved for ASCII characters
        # The last code is reserved for virtual EOF
        self._capacity = 2 ** code_bitsize - 1 - 256
        self._size = 0
        self._str_cache = set()

        for i in range(256):
            self._storage[i] = ascii2byte(i)
            self._str_cache.add(ascii2byte(i))

    __slots__ = ("_storage", "_capacity", "_size", "_str_cache")

    def clear(self) -> None:
        self._storage.clear()
        self._size = 0
        self._str_cache.clear()

        for i in range(256):
            self._storage[i] = ascii2byte(i)
            self._str_cache.add(ascii2byte(i))

    def __contains__(self, item: int) -> bool:
        return item in self._storage

    def __getitem__(self, key: int) -> bytes:
        if key not in self._storage:
            raise KeyError(f"Code not present in StrDict: {key}")
        return self._storage[key]

    def add_new_str(self, string: bytes) -> None:
        if string in self._str_cache:
            raise ValueError(f'string already in StrDict: "{string}"')

        self._storage[self._size + 256] = string
        self._size += 1
        self._str_cache.add(string)

        if self._size == self._capacity:
            self.clear()
