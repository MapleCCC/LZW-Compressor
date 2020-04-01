from typing import *

from .bit import Bit
from .convert_bytes_bits_int import *


# Mimic the interface of the builtin bytearray object
class Bitarray:
    def __init__(self, iterable: Iterable[Bit] = ()) -> None:
        self._storage: List[Bit] = list(iterable)

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

    def __eq__(self, other: "Bitarray") -> bool:
        return self._storage == other._storage

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
        """
        Boundary Conditions:
        empty bits yield 0
        """
        return bits2int(self._storage)

    @classmethod
    def from_int(cls, x: int, bit_size: int = None) -> "Bitarray":
        """
        Boundary Conditions:
        0 yields empty bitarray
        negative integers yield exception
        """
        _bits = int2bits(x)
        if bit_size:
            if bit_size < len(_bits):
                raise OverflowError
        else:
            bit_size = len(_bits)
        return cls([0] * (bit_size - len(_bits)) + _bits)

    def extend(self, iterable: Iterable[Bit]) -> None:
        self._storage.extend(iterable)

    # No need to have both push_bytes_back and push_byte_back. One interface suffices
    def push_bytes_back(self, bs: ByteString) -> None:
        self._storage.extend(bytes2bits(bs))

    # We can either implement pop_byte_front in terms of pop_bytes_from (top-down approach),
    # or implement pop_bytes_front in terms of pop_byte_front (bottom-up approach)
    def pop_byte_front(self) -> ByteString:
        if len(self._storage) < 8:
            raise IndexError("pop byte from bitarray with less than 8 bits")
        return self.pop_bytes_front(1)

    def pop_bytes_front(self, n: int = 1) -> ByteString:
        if len(self._storage) < 8 * n:
            raise IndexError(
                "pop bytes number exceeds bitarray's containing bytes' number"
            )
        bs = bits2bytes(self._storage[: 8 * n])
        self._storage = self._storage[8 * n :]
        return bs
