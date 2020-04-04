from typing import Dict

from .trie import Trie
from .utils import ascii2byte

# TODO: use trie as code dict internal data structure


# Encapsulate CodeDict data structure
# User doesn't know implementation detail
# We can change different internal data structure implementation without changing
# interface.
class CodeDict:
    def __init__(self, code_bitsize: int) -> None:
        if code_bitsize <= 8:
            raise ValueError("Code bit size should larger than 8")

        self._storage: Dict[bytes, int] = Trie()
        # The first 256 codes are reserved for ASCII characters
        # The last code is reserved for virtual EOF
        self._capacity = 2 ** code_bitsize - 256 - 1
        self._size = 0
        self._count = 0

        for i in range(256):
            self._storage[ascii2byte(i)] = i

    # Test if adding __slots__ actually accelerate or excerbate performance
    __slots__ = ("_storage", "_capacity", "_size", "_count")

    def clear(self) -> None:
        self._storage.clear()
        self._size = 0

        for i in range(256):
            self._storage[ascii2byte(i)] = i

    def __contains__(self, item: bytes) -> bool:
        """ Check string membership """
        return item in self._storage

    def __getitem__(self, key: bytes) -> int:
        try:
            return self._storage[key]
        except KeyError:
            raise KeyError(f'code is missing for string: "{key}"')

    def add_new_code(self, item: bytes) -> None:
        if self.__contains__(item):
            raise ValueError(f"{item} already in code dict")

        self._storage[item] = self._count + 256
        self._count += 1
        self._size += 1

        if self._size == self._capacity:
            self.clear()
