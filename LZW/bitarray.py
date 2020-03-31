import sys
from enum import Enum
from functools import partial, reduce
from itertools import chain
from typing import *

from .extra_itertools import iindex
from .pep467 import iterbytes


class Bit(Enum):
    ZERO = 0
    ONE = 1


# b'1' = b'\x31' -> 31
byte2int = partial(int.from_bytes, byteorder=sys.byteorder)
# b'1' = b'\x31' -> ['0','0','1','1','0','0','0','1']
byte2bits = lambda b: list(map(int, iter(format(byte2int(b), "b").rjust(8, "0"))))


# Mimic the interface of the builtin bytearray object
class Bitarray:
    def __init__(self, iterable: Iterable[Bit] = ()) -> None:
        self._storage: List[Bit] = list(iterable)

        # self._bit_load_size = 0

    __slots__ = ["_storage"]

    def __getitem__(self, key: Union[int, slice]) -> Union[Bit, "Bitarray"]:
        if isinstance(key, int):
            return Bit(self._storage[key])
        elif isinstance(key, slice):
            return Bitarray(self._storage[key])
        else:
            raise TypeError

    def __len__(self) -> int:
        """ Return bit number """
        return len(self._storage)

    def __str__(self) -> str:
        if len(self._storage) > 20:
            return f"Bitarray({str(self._storage[:10])[:-1]}...{str(self._storage[-10:])[1:]})"
        else:
            return self.__repr__()

    # Ensure that eval(repr(x)) == x
    def __repr__(self) -> str:
        return f"Bitarray({self._storage})"

    def __add__(self, other: "Bitarray") -> "Bitarray":
        if not isinstance(other, Bitarray):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Bitarray' and {type(other)}"
            )
        return Bitarray(self._storage + other._storage)

    def __iadd__(self, other: "Bitarray") -> "Bitarray":
        if not isinstance(other, Bitarray):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Bitarray' and {type(other)}"
            )
        self._storage.extend(other._storage)
        return self

    def to_int(self) -> int:
        if not self._storage:
            raise IndexError("can't convert empty bitarray to int")

        # Small optimization trick
        most_significant_bit_index = iindex(self._storage, 1)
        return reduce(
            lambda x, y: 2 * x + y, self._storage[most_significant_bit_index:], 0
        )

    @classmethod
    def from_int(cls, x: int, bit_size: int) -> "Bitarray":
        return cls(map(int, format(x, "b").rjust(bit_size, "0")))

    def extend(self, iterable: Iterable[Bit]) -> None:
        self._storage.extend(iterable)

    # No need to have both push_bytes_back and push_byte_back. One interface suffices
    def push_bytes_back(self, bs: ByteString) -> None:
        self._storage.extend(chain(*map(byte2bits, iterbytes(bs))))

    # We can either implemnt pop_byte_front in terms of pop_bytes_from (top-down approach),
    # or implement pop_bytes_front in terms of pop_byte_front (bottom-up approach)
    def pop_byte_front(self) -> bytes:
        if len(self._storage) < 8:
            raise IndexError("pop byte from bitarray with less than 8 bits")

        byte = self[:8].to_int().to_bytes(1, sys.byteorder)
        self._storage = self._storage[8:]
        return byte

    def pop_bytes_front(self, n: int) -> Iterator[bytes]:
        if len(self._storage) <= 8 * n:
            raise IndexError(
                "pop bytes number exceeds bitarray's containing bytes' number"
            )
        for _ in range(n):
            yield self.pop_byte_front()
