from typing import AnyStr, Callable

from .extra_itertools import iequal
from .iostream import FileInStreamer


def undecorate(func: Callable) -> Callable:
    ret = func
    while True:
        try:
            ret = ret.__wrapped__
        except AttributeError:
            break
    return ret


def ascii2byte(x: int) -> bytes:
    if not 0 <= x <= 255:
        raise ValueError
    return x.to_bytes(1, "big")


def byte2ascii(b: bytes) -> int:
    if len(b) != 1:
        raise ValueError
    return int.from_bytes(b, "big")
