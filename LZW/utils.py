import sys
from typing import *

from .extra_itertools import iequal
from .iostream import FileInStreamer


def is_equal_file(*filenames, mode: str = "r", **kwargs) -> int:
    fs_itr = (FileInStreamer(filename, mode, **kwargs) for filename in filenames)
    return iequal(*fs_itr)


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
    return x.to_bytes(1, sys.byteorder)


def byte2ascii(b: ByteString) -> int:
    if len(b) > 1:
        raise ValueError
    return int.from_bytes(b, sys.byteorder)
