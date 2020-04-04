from itertools import chain, tee
from typing import *

from hypothesis import assume, given
from hypothesis.strategies import integers, lists, iterables

from LZW.extra_itertools import *


@given(iterables(integers()), integers(min_value=0, max_value=10))
def test_iequal(l: Iterable[int], n: int) -> None:
    itrs = tee(l, n)
    assert iequal(*itrs)


@given(lists(integers()), lists(integers()), integers(min_value=1, max_value=10))
def test_iequal_on_non_equal_iterables(l1: List[int], l2: List[int], n: int) -> None:
    assume(l1 != l2)
    itr1, itr2 = iter(l1), iter(l2)
    itrs = chain(tee(itr1, n), [itr2])
    assert not iequal(*itrs)


@given(iterables(integers()), integers())
def test_iappend(l: Iterable[int], x: int) -> None:
    l1, l2 = tee(l)
    assert list(iappend(l1, x)) == list(l2) + [x]
