from typing import *

import pytest
from hypothesis import given
from hypothesis.strategies import binary, integers, iterables, sampled_from

from LZW.convert_bytes_bits_int import *
from LZW.bit import Bit

# It happens that we can not use property-based test framework here.
# Manual test cases are needed, instead.

bits = sampled_from(Bit)

# @given(integers())
# def test_int(x: int) -> None:
#     if x == 0:
#         assert int2bytes(x) == b""
#     elif x < 0:
#         with pytest.raises(Exception):
#             int2bytes(x)
#     else:
#         assert bytes2int(int2bytes(x)) == x
#         assert bits2int(int2bits(x)) == x
#         assert bytes2int(bits2bytes(int2bits(x))) == x
#         assert bits2int(bytes2bits(int2bytes(x))) == x


# @given(binary())
# def test_bytes(bs: ByteString) -> None:
#     if not bs:
#         assert bytes2int(bs) == 0
#         assert list(bytes2bits(bs)) == []
#     else:
#         assert int2bytes(bytes2int(bs)) == bs
#         assert bits2bytes(bytes2bits(bs)) == bs
#         assert int2bytes(bits2int(bytes2bits(bs))) == bs
#         assert bits2bytes(int2bits(bytes2int(bs))) == bs


# @given(iterables(bits))
# def test_non_empty_bits(bits: Iterable[Bit]) -> None:
#     assert bytes2bits(bits2bytes(bits)) == bits
#     assert int2bits(bits2int(bits)) == bits
#     assert int2bits(bytes2int(bits2bytes(bits))) == bits
#     assert bytes2bits(int2bytes(bits2int(bits))) == bits


# def test_empty_bits(bits: Iterable[Bit] = ()) -> None:
#     assert bits2int(bits) == 0
#     assert bits2bytes(bits) == b""
