import math
import sys
from functools import reduce
from typing import *

from .bit import Bit
from .extra_itertools import grouper
from .pep467 import iterbytes

# For now, we don't consider negative numbers
# We may add `signed` argument later on


def most_significant_bit_number(x: int) -> int:
    """
    Boundary Conditions:
    0 results in 0
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    if x == 0:
        return 0
    return math.floor(math.log2(x)) + 1


# 31 -> b'\x31'
def int2bytes(x: int) -> ByteString:
    """
    Different from builtin int.to_bytes in that there is no positional
    arguments: length and byteorder. This function will automatically
    determine the least length that can contain the most significant
    bit.

    Boundary Conditions:
    0 results in empty bytes
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    min_byte_num = math.ceil(most_significant_bit_number(x) / 8)
    return x.to_bytes(min_byte_num, sys.byteorder)


# b'1' = b'\x31' -> 31
def bytes2int(bs: ByteString) -> int:
    """
    Boundary Conditions:
    empty bytes results in 0
    """
    return int.from_bytes(bs, sys.byteorder)


# b'1' = b'\x31' -> ['0','0','1','1','0','0','0','1']
def bytes2bits(bs: ByteString) -> Iterator[Bit]:
    for b in iterbytes(bs):
        for s in format(bytes2int(b), "b").rjust(8, "0"):
            yield Bit(int(s))


# (0,0,1,1,0,0,0,1) -> b'1'
def bits2bytes(bits: Iterable[Bit]) -> ByteString:
    """
    If bits number is not multiple of eight, 0 is filled at the end

    Boundary Conditions:
    empty input yields empty bytes
    """
    bits = list(bits)
    if len(bits) % 8 != 0:
        raise ValueError("bits number needs to be multiples of eight")
    # ret = b""
    # for eight_bits in grouper(bits, 8, fillvalue=0):
    #     ret += int2bytes(reduce(lambda x, y: 2 * x + y, eight_bits, 0))
    # return ret
    return int2bytes(bits2int(bits))


# (0,0,1,1,0,0,0,1) -> 31
def bits2int(bits: Iterable[Bit]) -> int:
    """
    Boundary Conditions:
    Empty input results in 0
    """
    return reduce(lambda x, y: x * 2 + y, bits, 0)


# 31 -> (0,0,1,1,0,0,0,1)
def int2bits(x: int) -> Iterator[Bit]:
    """
    Boundary Conditions:
    0 yields empty output
    negative integers yield exception
    """
    if x < 0:
        raise NotImplementedError
    return bytes2bits(int2bytes(x))
