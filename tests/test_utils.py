import functools

from LZW.utils import undecorate


def test_undecorate():
    def get_two(func):
        return functools.wraps(func)(lambda: 2)

    def get_one(func):
        return functools.wraps(func)(lambda: 1)

    @get_two
    @get_one
    def raw():
        return 0

    assert undecorate(raw)() == 0
