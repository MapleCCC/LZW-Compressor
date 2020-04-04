from itertools import chain, zip_longest
from typing import Any, Callable, Iterable

from more_itertools import all_equal

__all__ = [
    "iappend",
    "iequal",
]


def iappend(iterable: Iterable, tail: Any) -> Iterable:
    return chain(iterable, [tail])


def iequal(*iterables: Iterable) -> bool:
    """ Test if all iterable objects have identical contents """
    _sentinel = object()
    zipped = zip_longest(*iterables, fillvalue=_sentinel)
    return all(map(lambda x: all_equal(x), zipped))


_iequal_from_iterable: Callable[[Iterable[Iterable]], bool] = lambda iterables: iequal(
    *iterables
)

iequal.from_iterable = _iequal_from_iterable
