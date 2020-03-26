import random

from .extra_itertools import iequal
from .iostream import FileInStreamer


def generate_gibberish(length: int, charset) -> str:
    assert length >= 0
    return "".join(random.choices(charset, k=length))


def generate_gibberish_file(filename: str, length: int, charset) -> None:
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(generate_gibberish(length, charset))


def is_equal_file(*filenames, mode: str = "r", **kwargs) -> int:
    fs_itr = (FileInStreamer(filename, mode, **kwargs) for filename in filenames)
    return iequal(*fs_itr)
