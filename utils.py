import itertools
from typing import *


def read_file_content(
    filename: str, is_binary: bool = False, **kwargs
) -> Union[str, bytes]:
    if not is_binary:
        with open(filename, "r", encoding="utf-8", **kwargs) as f:
            return f.read()
    else:
        with open(filename, "rb", **kwargs) as f:
            return f.read()


def write_file_content(
    filename: str, text: Union[str, bytes], is_binary: bool = False, **kwargs
) -> None:
    if not is_binary:
        with open(filename, "w", encoding="utf-8", **kwargs) as f:
            f.write(text)
    else:
        with open(filename, "wb", **kwargs) as f:
            f.write(text)


def diff_file(filename1: str, filename2: str, is_binary: bool = False, **kwargs) -> int:
    content1 = read_file_content(filename1, is_binary, **kwargs)
    content2 = read_file_content(filename2, is_binary, **kwargs)
    return content1 == content2


def isplit(l: Iterable, sep) -> Iterator[List]:
    stream = iter(l)
    sublist = list(itertools.takewhile(lambda x: x != sep, stream))
    while sublist:
        yield sublist
        sublist = list(itertools.takewhile(lambda x: x != sep, stream))
