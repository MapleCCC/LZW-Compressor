from typing import Dict

# TODO: add max_len restriction to code dict
# TODO: reserve the last code of code dict as virtual EOF
# TODO: use trie as code dict internal data structure


# Encapsulate CodeDict data structure
# User doesn't know implementation detail
# We can change different internal data structure implementation without changing
# interface.
class CodeDict:
    def __init__(self, code_bit: int) -> None:
        self._storage: Dict[str, int] = dict()
        # The first 256 codes are reserved for ASCII characters
        # The last code is reserved for virtual EOF
        self._capacity = 2 ** code_bit - 256 - 1
        self._size = 0

        for i in range(256):
            self._storage[chr(i)] = i

    # Test if adding __slots__ actually accelerate or excerbate performance
    __slots__ = ("_storage", "_capacity", "_size")

    def clear(self) -> None:
        self._storage.clear()
        self._size = 256

        for i in range(256):
            self._storage[chr(i)] = i

    def __contains__(self, item) -> bool:
        """ Check string membership """
        return item in self._storage

    def __getitem__(self, key) -> int:
        try:
            return self._storage[key]
        except:
            raise KeyError(f"code is missing for: {key}")

    def add_new_code(self, item) -> None:
        if self.__contains__(item):
            raise ValueError(f"{item} already in code dict")

        if self._size == self._capacity:
            raise NotImplementedError
            # self.clear()

        self._storage[item] = self._size + 256
        self._size += 1
