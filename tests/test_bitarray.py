import pytest
from hypothesis import given
from hypothesis.strategies import binary, integers, just

from LZW.bitarray import Bitarray
from LZW.utils import ascii2byte


@given(integers(min_value=0))
def test_int_conversion(x: int) -> None:
    assert Bitarray.from_int(x).to_int() == x


@given(binary())
def test_int_conversion_reverse(bs: bytes):
    ba = Bitarray()
    ba.push_bytes_back(bs)
    assert Bitarray.from_int(ba.to_int()).to_int() == ba.to_int()


@given(binary(min_size=1))
def test_push_pop(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    for i in range(len(bs)):
        assert ba.pop_byte_front() == ascii2byte(bs[i])


@given(just(b""))
def test_push_pop_empty_input(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    with pytest.raises(IndexError):
        ba.pop_byte_front()


@given(binary())
def test_len(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    assert len(ba) == 8 * len(bs)


@given(binary(), binary())
def test_iadd(bs1: bytes, bs2: bytes) -> None:
    ba1 = Bitarray()
    ba1.push_bytes_back(bs1)
    ba2 = Bitarray()
    ba2.push_bytes_back(bs2)
    ba1 += ba2

    assert len(ba1) == 8 * (len(bs1) + len(bs2))

    bs3 = bs1 + bs2
    for i in range(len(bs3)):
        assert ba1.pop_byte_front() == ascii2byte(bs3[i])


@given(binary(min_size=1))
def test_slice(bs: bytes) -> None:
    ba = Bitarray()
    ba.push_bytes_back(bs)
    ba1 = ba
    assert ba1[:8].pop_byte_front() == ba1.pop_byte_front()
    ba2 = ba
    assert ba2[:] == ba2
    # ba3 = ba
    # TODO: more test cases
