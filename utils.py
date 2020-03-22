import itertools
from typing import *


def read_file_content(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file_content(filename: str, text: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def diff_file(filename1: str, filename2: str) -> int:
    content1 = read_file_content(filename1)
    content2 = read_file_content(filename2)
    return content1 == content2


def isplit(l: Iterable, sep) -> Iterator[List]:
    stream = iter(l)
    sublist = list(itertools.takewhile(lambda x: x != sep, stream))
    while sublist:
        yield sublist
        sublist = list(itertools.takewhile(lambda x: x != sep, stream))
