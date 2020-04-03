from itertools import takewhile, zip_longest
from typing import *

from more_itertools import all_equal, ilen

__all__ = [
    "iindex",
    "EmptyTailError",
    "NotReachedTailError",
    "remove_tail",
    "ijoin",
    "iequal",
    "takeuntil",
]


def iindex(iterable: Iterable, target) -> int:
    """ If the target is not in iterable, length of the iterable will be returned. """
    return ilen(takewhile(lambda x: x != target, iterable))


class EmptyTailError(Exception):
    pass


class NotReachedTailError(Exception):
    pass


# Consider use itertools.tee and more_itertools.tail to simplify tail storage logic.

# class disguised as function/callable
class remove_tail:
    """
    Store tail in iterator object's attribute named "tail", for later refernce.

    Be aware that the tail storing behavior may give you surprising result when
    you expect some references to be garbage collected.
    """

    # If passed in an zero-length iterable, which means there exists no tail, a class
    # level constant singleton _TAIL_EMPTY_SENTINEL would be stored in tail instead.

    _TAIL_EMPTY_SENTINEL = object()

    def __init__(self, iterable: Iterable, n: int = 1) -> None:
        if n != 1:
            raise NotImplementedError

        self._past = self.__class__._TAIL_EMPTY_SENTINEL
        self._internal_iterator = enumerate(iterable)
        self._reached_tail = False

    def __next__(self) -> Any:
        try:
            i, elem = next(self._internal_iterator)
            if i == 0:
                self._past = elem
                ret = self._past
                _, second_elem = next(self._internal_iterator)
                self._past = second_elem
                return ret
            else:
                ret = self._past
                self._past = elem
                return ret
        except StopIteration:
            self._reached_tail = True
            raise

    def __iter__(self) -> Iterator:
        return self

    def reached_tail(self) -> bool:
        return self._reached_tail

    def has_empty_tail(self) -> bool:
        return self._past is self.__class__._TAIL_EMPTY_SENTINEL

    @property
    def tail(self) -> Any:
        if not self._reached_tail:
            raise NotReachedTailError("Not yet reached tail")
        if self.has_empty_tail():
            raise EmptyTailError("Empty iterable has no tail")
        return self._past


def ijoin(separator: Iterable, iterables: Iterable[Iterable]) -> Iterable:
    sep = list(separator)
    new_iterator = remove_tail(iterables)
    for iterable in new_iterator:
        yield from iterable
        yield from sep
    if new_iterator.reached_tail() and not new_iterator.has_empty_tail():
        yield from new_iterator.tail


def iequal(*iterables) -> int:
    """ Test if all iterable objects have identical contents """
    _sentinel = object()
    zipped = zip_longest(*iterables, fillvalue=_sentinel)
    return all(map(lambda x: all_equal(x), zipped))


def takeuntil(iterable: Iterable, sentinel: Any) -> Iterator:
    stop_signal = False
    for elem in iterable:
        if elem == sentinel:
            stop_signal = True
        yield elem
        if stop_signal:
            return
