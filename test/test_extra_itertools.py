import random
from itertools import tee, chain
from typing import *

from hypothesis import given
from hypothesis.strategies import characters, integers, lists, none, text

from LZW.extra_itertools import *


@given(lists(integers()))
def test_remove_tail(l: List[int]) -> None:
    new_iterator = remove_tail(iter(l))
    assert list(new_iterator) == l[:-1]
    if new_iterator.reached_tail() and not new_iterator.has_empty_tail():
        assert new_iterator.tail == l[-1]


@given(text(), characters())
def test_isplit(s: str, char: str) -> None:
    # charset = set(s)
    # for char in charset:
    #     a = isplit(list(s), char)
    #     b = s.split(char)
    #     for c, d in zip(a, b):
    #         assert list(c) == list(d)

    a = isplit(list(s), char)
    b = s.split(char)
    for c, d in zip(a, b):
        assert list(c) == list(d)


@given(text(), lists(text()))
def test_ijoin(sep: str, str_list: List[str]) -> None:
    assert list(ijoin(sep, str_list)) == list(sep.join(str_list))


@given(integers(), integers(), lists(none()))
def test_all_equal(x: int, y: int, l: List[None]) -> None:
    for i in range(len(l)):
        l[i] = x
    assert all_equal(l)
    if len(l) >= 2:
        if x == y:
            y += 1
        l[random.randrange(len(l))] = y
        assert not all_equal(l)


@given(lists(integers()), lists(integers()), integers(min_value=0, max_value=10))
def test_iequal(l: List[int], l2: List[int], n: int) -> None:
    itrs = tee(l, n)
    assert iequal(*itrs)
    if l == l2:
        l2.append(1)
    if n > 0:
        itrs = chain(tee(l, n), [l2])
        assert not iequal(*itrs)
