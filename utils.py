import random
from itertools import groupby, zip_longest
from typing import *

from iostream import FileInStreamer


def generate_gibberish(length: int, charset) -> str:
    assert length >= 0
    return "".join(random.choices(charset, k=length))


def generate_gibberish_file(filename: str, length: int, charset) -> None:
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(generate_gibberish(length, charset))


def is_equal_file(*filenames, mode: str = "r", **kwargs) -> int:
    return iequal(FileInStreamer(filename, mode, **kwargs) for filename in filenames)


# The all_equal function comes from more-itertools library
def all_equal(iterable: Iterable) -> bool:
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


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
