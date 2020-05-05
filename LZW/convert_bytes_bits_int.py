import math
from functools import reduce
from typing import Iterable, Iterator, List

from more_itertools import grouper

from .bit import Bit
from .pep467 import iterbytes
from .utils import ascii2byte, byte2ascii

# For now, we don't consider negative numbers
# We may add `signed` argument later on

# For now, we default to big-endian byteorder. This simplifies program.


def most_significant_bit_number(x: int) -> int:
    """
    Boundary Conditions:
    0 results in 1
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    return x.bit_length()


# 31 -> b'\x31'
def int2bytes(x: int) -> bytes:
    """
    Different from builtin int.to_bytes in that there is no positional
    arguments: length and byteorder. This function will automatically
    determine the least length that can contain the most significant
    bit.

    Boundary Conditions:
    0 results in b"\x00"
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    min_byte_num = math.ceil(most_significant_bit_number(x) / 8)
    return x.to_bytes(min_byte_num, "big")


# b'1' = b'\x31' -> 31
def bytes2int(bs: bytes) -> int:
    """
    Boundary Conditions:
    empty bytes yield 0
    """
    return int.from_bytes(bs, "big")


# b'1' = b'\x31' -> [1,1,0,0,0,1]
def bytes2bits(bs: bytes) -> Iterator[Bit]:
    """ Empty bytes yield empty output """
    for byte in iterbytes(bs):
        bits = int2bits(byte2ascii(byte))
        yield from [0] * (8 - len(bits)) + bits


# (0,0,1,1,0,0,0,1) -> b'1'
def bits2bytes(bits: Iterable[Bit]) -> bytes:
    """
    If bits number is not multiple of eight, exception is raised.

    Boundary Conditions:
    empty input yields empty bytes
    """
    bit_list = list(bits)
    if len(bit_list) % 8 != 0:
        raise ValueError("bits number needs to be multiples of eight")
    ret = b""
    for eight_bits in grouper(bit_list, 8):
        ret += ascii2byte(bits2int(eight_bits))
    return ret


# (1,1,0,0,0,1) -> 31
def bits2int(bits: Iterable[Bit]) -> int:
    """
    Boundary Conditions:
    Empty input results in 0
    """
    return reduce(lambda x, y: x * 2 + y, bits, 0)


# 31 -> (1,1,0,0,0,1)
def int2bits(x: int) -> List[Bit]:
    """
    Boundary Conditions:
    0 yields empty output
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    remainders = []
    while x != 0:
        remainders.append(x % 2)
        x = x // 2
    return remainders[::-1]
