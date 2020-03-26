import os
import string
import uuid
from typing import List

from hypothesis import given
from hypothesis.strategies import integers, lists, text

from LZW.lzwfile import *

# Reference: https://en.wikipedia.org/wiki/Filename#Comparison_of_filename_limitations
portable_filename_alphabet = string.ascii_letters + string.digits + "._-"


@given(l=lists(text(portable_filename_alphabet, min_size=1)))
def test_lzwfile_header(l: List[str], tmp_path):
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    write_lzwfile_header("file", l)
    assert list(read_lzwfile_header("file")) == l


CODE_BIT = 12
MAX_CODE = 2 ** CODE_BIT - 1


@given(l=lists(integers(min_value=0, max_value=MAX_CODE)))
def test_lzwfile_codes(l: List[int], tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    write_lzwfile_codes("file", l, CODE_BIT)
    assert list(read_lzwfile_codes("file", CODE_BIT)) == l
