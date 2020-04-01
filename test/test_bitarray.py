from typing import *

import pytest
from hypothesis import given
from hypothesis.strategies import binary, integers, iterables

from LZW.bitarray import Bitarray


@given(integers(min_value=0))
def test_int_conversion(x: int) -> None:
    assert Bitarray.from_int(x).to_int() == x


@given(iterables(integers(min_value=0, max_value=1)))
def test_int_conversion_reverse(l: Iterable[int]):
    b = Bitarray(l)
    assert Bitarray.from_int(b.to_int()) == b


@given(binary())
def test_push_pop(bs: ByteString) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    if len(bs) > 0:
        assert ba.pop_byte_front() == bs[0]
        ba.push_bytes_back(bs)
        assert ba.pop_bytes_front(len(bs)) == bs
    else:
        with pytest.raises(IndexError):
            ba.pop_byte_front()
        with pytest.raises(IndexError):
            ba.pop_bytes_front()


def test_repr():
    pass
