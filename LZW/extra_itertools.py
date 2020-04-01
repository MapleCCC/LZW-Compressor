from itertools import groupby, takewhile, zip_longest
from typing import *

__all__ = [
    "iindex",
    "ilen",
    "remove_tail",
    "ijoin",
    "all_equal",
    "iequal",
    "iter_noexcept",
    "isplit",
    "takeuntil",
]


# grouper function code snippet comes from https://docs.python.org/3.8/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def iindex(iterable: Iterable, target) -> int:
    return ilen(takewhile(lambda x: x != target, iterable))


def ilen(iterable: Iterable) -> int:
    count = 0
    for _ in iterable:
        count += 1
    return count


class EmptyTailError(Exception):
    pass


class NotReachedTailError(Exception):
    pass


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


# all_equal function code snippet comes from https://docs.python.org/3.8/library/itertools.html#itertools-recipes
def all_equal(iterable: Iterable) -> bool:
    "Returns True if all the elements are equal to each other"
    g = groupby(iterable)
    return next(g, True) and not next(g, False)  # type: ignore


def iequal(*iterables) -> int:
    """ Find if contents of all iterables are equal """
    _sentinel = object()
    zipped = zip_longest(*iterables, fillvalue=_sentinel)
    return all(map(lambda x: all_equal(x), zipped))


StopIterationDummyObject = object()


def iter_noexcept(l: Iterable) -> Iterator:
    """
    An iterator wrapper, instead of raising exception on exhausion,
    yields StopIterationDummyObject.
    """
    stream = iter(l)
    while True:
        yield next(stream, StopIterationDummyObject)

    # yield from iter(l)
    # while True:
    #     yield StopIterationDummyObject


# def takewhile_except(iterable: Iterable, sentinel: Any) -> Iterator:
#     count = 0
#     for elem in iterable:
#         count += 1
#         if elem != sentinel:
#             yield elem
#         else:
#             return
#     if count == 0:
#         raise CustomExcept


def isplit(l: Iterable, sep) -> Iterator[Iterable]:
    # Impl 1:
    # stream = iter_noexcept(l)
    # buffer = []
    # for elem in stream:
    #     if elem is StopIterationDummyObject:
    #         break
    #     if elem != sep:
    #         buffer.append
    #     else:
    #         yield buffer
    #         buffer.clear()

    # Impl 2:
    # stream = iter(l)
    # buffer = []
    # try:
    #     for elem in stream:
    #         if elem != sep:
    #             buffer.append(elem)
    #         else:
    #             yield buffer
    #             buffer.clear()
    # except StopIteration:
    #     yield buffer

    # Impl 3:
    # If implemented this way, the isplit function returns a
    # generator object that is not able to be passed to list()
    stream = iter(l)
    stop_iteration_signal = 0

    def generate_split():
        nonlocal stop_iteration_signal

        for elem in stream:
            if elem != sep:
                yield elem
            else:
                return

        stop_iteration_signal = 1
        return

    while not stop_iteration_signal:
        yield generate_split()

    # Impl 4:
    # takewhile_except


if __name__ == "__main__":
    l = [1, 2, 3, 2, 3, 3]
    s = isplit(l, 3)
    a = next(s)
    print(list(a))
    a = next(s)
    print(list(a))
    a = next(s)
    print(list(a))
    a = next(s)
    print(list(a))
    a = next(s)
    print(list(a))


def takeuntil(iterable: Iterable, sentinel: Any) -> Iterator:
    stop_signal = False
    for elem in iterable:
        if elem == sentinel:
            stop_signal = True
        yield elem
        if stop_signal:
            return
