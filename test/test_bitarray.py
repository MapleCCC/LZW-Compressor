from typing import Iterable

import pytest
from hypothesis import given
from hypothesis.strategies import binary, integers, iterables, just, sampled_from

from LZW.bitarray import Bitarray
from LZW.utils import ascii2byte
from LZW.bit import Bit

bits = sampled_from(Bit)


@given(integers(min_value=0))
def test_int_conversion(x: int) -> None:
    assert Bitarray.from_int(x).to_int() == x


@given(iterables(bits))
def test_int_conversion_reverse(l: Iterable[Bit]):
    b = Bitarray(l)
    assert Bitarray.from_int(b.to_int()).to_int() == b.to_int()


@given(binary(min_size=1))
def test_push_pop(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    assert ba.pop_byte_front() == ascii2byte(bs[0])
    assert ba.pop_bytes_front(len(bs) - 1) == bytearray(bs)[1:]


@given(just(b""))
def test_push_pop_empty_input(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    with pytest.raises(IndexError):
        ba.pop_byte_front()
    with pytest.raises(IndexError):
        ba.pop_bytes_front()


@given(iterables(bits))
def test_repr(l: Iterable[Bit]):
    b = Bitarray(l)
    assert eval(repr(b)) == b
