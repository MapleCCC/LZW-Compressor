# TODO: remove the future statement in Python 4.0
from __future__ import annotations

from functools import singledispatchmethod
from typing import NoReturn

from .bit import Bit


# Mimic the interface of the builtin bytearray object
class Bitarray:
    def __init__(self) -> None:
        self._data = 0
        self._size = 0

    __slots__ = ["_data", "_size"]

    @singledispatchmethod
    def __getitem__(self, index: object) -> NoReturn:
        raise TypeError

    @__getitem__.register
    def _(self, index: int) -> Bit:
        return Bit((self._data >> (self._size - index - 1)) & 1)

    # TODO: change type hint "Bitarray" to Bitarray after the bug of incompatibility
    # between functools.singledispatchmethod and __future__.annotations is resolved.
    @__getitem__.register
    def _(self, index: slice) -> "Bitarray":
        start, stop = index.start, index.stop
        if start is None:
            start = 0
        if stop is None:
            stop = self._size
        if start < 0:
            start += self._size
        if stop < 0:
            stop += self._size

        if not (start <= stop and start < self._size and stop <= self._size):
            return Bitarray()

        mask = (1 << (stop - start)) - 1
        ret = Bitarray()
        ret._data = (self._data >> (self._size - stop)) & mask
        ret._size = stop - start
        return ret

    def __len__(self) -> int:
        """ Return bit number """
        return self._size

    def __str__(self) -> str:
        repre = self.__repr__()
        if self._size > 20:
            return "Bitarray({}...{})".format(repre[:10], repre[-10:])
        else:
            return repre

    def __repr__(self) -> str:
        return "Bitarray({})".format(format(self._data, "b"))

    def __eq__(self, other: Bitarray) -> bool:
        return self._data == other._data and self._size == other._size

    def __iadd__(self, other: Bitarray) -> Bitarray:
        if not isinstance(other, Bitarray):
            raise TypeError(
                f"unsupported operand type(s) for +: 'Bitarray' and {type(other)}"
            )
        self._data = (self._data << other._size) + other._data
        self._size += other._size
        return self

    def to_int(self) -> int:
        """
        Boundary Conditions:
        empty bits yield 0
        """
        return self._data

    @classmethod
    def from_int(cls, x: int, bit_size: int = None) -> Bitarray:
        """
        Boundary Conditions:
        0 yields empty bitarray
        negative integers yield exception
        """
        if x < 0:
            raise NotImplementedError

        canonical_bit_len = x.bit_length()
        if bit_size:
            if bit_size < canonical_bit_len:
                raise OverflowError
        else:
            bit_size = canonical_bit_len

        ret = Bitarray()
        ret._data = x
        ret._size = bit_size
        return ret

    # No need to have both push_bytes_back and push_byte_back. One interface suffices
    def push_bytes_back(self, bs: bytes) -> None:
        for byte in bs:
            self._data = (self._data << 8) + byte
            self._size += 8

    # We can either implement pop_byte_front in terms of pop_bytes_from (top-down approach),
    # or implement pop_bytes_front in terms of pop_byte_front (bottom-up approach)
    def pop_byte_front(self) -> bytes:
        if self._size < 8:
            raise IndexError("pop byte from bitarray with less than 8 bits")
        ret = (self._data >> (self._size - 8)).to_bytes(1, "big")
        self._data &= (1 << (self._size - 8)) - 1
        self._size -= 8
        return ret
