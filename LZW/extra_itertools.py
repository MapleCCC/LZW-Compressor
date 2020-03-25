from typing import *
from itertools import groupby, zip_longest


TAIL_EMPTY_SENTINEL = object()


def remove_tail(iterable: Iterable, n: int = 1, store_tail: bool = True) -> Iterator:
    """
    Store tail in function object's attribute named "tail", for later refernce.

    You can ask it to not store the tail, so as to save space,
    by setting parameter store_tail to False.

    Be aware that the tail storing behavior may give you surprising result when
    you expect some references to be garbage collected.

    If passed in an zero-length iterable, which means there is no tail, a singleton
    TAIL_EMPTY_SENTINEL would be stored in remove_tail.tail instead.
    """
    if n != 1:
        raise NotImplementedError

    lookahead = TAIL_EMPTY_SENTINEL
    for i, elem in enumerate(iterable):
        if i != 0:
            yield lookahead
        lookahead = elem

    if store_tail:
        remove_tail.tail = lookahead


def ijoin(separator: Iterable, iterables: Iterable[Iterable]) -> Iterable:
    sep = list(separator)
    for iterable in remove_tail(iterables):
        yield from iterable
        yield from sep
    if remove_tail.tail != TAIL_EMPTY_SENTINEL:
        yield from remove_tail.tail


# The all_equal function comes from more-itertools library
def all_equal(iterable: Iterable) -> bool:
    g = groupby(iterable)
    return next(g, True) and not next(g, False)  # type: ignore


def iequal(*iterables) -> int:
    """ Find if contents of all iterables are equal """
    _sentinel = object()
    zipped = zip_longest(iterables, fillvalue=_sentinel)
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
