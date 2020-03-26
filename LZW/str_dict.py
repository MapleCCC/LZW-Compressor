from typing import Dict


class StrDict:
    def __init__(self, code_bit: int) -> None:
        self._storage: Dict[int, str] = {}
        # The first 256 codes are reserved for ASCII characters
        # The last code is reserved for virtual EOF
        self._capacity = 2 ** code_bit - 1 - 256
        self._size = 0
        self._count = 0

        for i in range(256):
            self._storage[i] = chr(i)

    __slots__ = ("_storage", "_capacity", "_size", "_count")

    def clear(self) -> None:
        self._storage.clear()
        self._size = 0

        for i in range(256):
            self._storage[i] = chr(i)

    def __contains__(self, item: int) -> bool:
        # """ A versatile membership testing routine """
        # if isinstance(item, int):
        #     return item in self._storage
        # elif isinstance(item, str):
        #     return item in self._storage.values()
        # else:
        #     raise TypeError
        return item in self._storage

    def __getitem__(self, key: int) -> str:
        if key not in self._storage:
            raise KeyError(f"Code not present in StrDict: {key}")
        return self._storage[key]

    def add_new_str(self, string: str) -> None:
        if string in self._storage.values():
            raise ValueError(f'string already in StrDict: "{string}"')

        self._storage[self._size + 256] = string
        self._size += 1

        if self._size == self._capacity:
            self.clear()
