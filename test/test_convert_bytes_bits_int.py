from typing import *

import pytest
from hypothesis import given
from hypothesis.strategies import binary, integers, iterables

from LZW.convert_bytes_bits_int import *


@given(integers(min_value=0))
def test_most_significant_bit_number(x: int) -> None:
    if x == 0:
        assert most_significant_bit_number(x) == 0
    else:
        assert len(format(x, "b")) == most_significant_bit_number(x)


@given(integers())
def test_int(x: int) -> None:
    if x == 0:
        assert int2bytes(x) == b""
    elif x < 0:
        with pytest.raises(Exception):
            int2bytes(x)
    else:
        assert bytes2int(int2bytes(x)) == x
        assert bits2int(int2bits(x)) == x
        assert bytes2int(bits2bytes(int2bits(x))) == x
        assert bits2int(bytes2bits(int2bytes(x))) == x


@given(binary())
def test_bytes(bs: ByteString) -> None:
    assert int2bytes(bytes2int(bs)) == bs
    assert bits2bytes(bytes2bits(bs)) == bs
    assert int2bytes(bits2int(bytes2bits(bs))) == bs
    assert bits2bytes(int2bits(bytes2int(bs))) == bs


@given(iterables(integers(min_value=0, max_value=1)))
def test_bits(bits: Iterable[Bit]) -> None:
    assert bytes2bits(bits2bytes(bits)) == bits
    assert int2bits(bits2int(bits)) == bits
    assert int2bits(bytes2int(bits2bytes(bits))) == bits
    assert bytes2bits(int2bytes(bits2int(bits))) == bits
