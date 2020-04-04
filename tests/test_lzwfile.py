import os
import string
import uuid
from itertools import tee
from typing import Iterable

from hypothesis import given
from hypothesis.strategies import integers, iterables, text

from LZW.lzwfile import (
    Code,
    Header,
    read_lzwfile_codes,
    read_lzwfile_header,
    write_lzwfile_codes,
    write_lzwfile_header,
)

# Reference: https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations
portable_filename_alphabet = string.ascii_letters + string.digits + "._-"


@given(l=iterables(text(portable_filename_alphabet, min_size=1)))
def test_lzwfile_header(l: Header, tmp_path):
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    l1, l2 = tee(l)

    write_lzwfile_header("file", l1)
    assert list(read_lzwfile_header("file")) == list(l2)


CODE_BITSIZE = 12
MAX_CODE = 2 ** CODE_BITSIZE - 1


@given(l=iterables(integers(min_value=0, max_value=MAX_CODE)))
def test_lzwfile_codes(l: Iterable[Code], tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    l1, l2 = tee(l)

    write_lzwfile_codes("file", l1, CODE_BITSIZE)
    assert list(read_lzwfile_codes("file", CODE_BITSIZE)) == list(l2)
