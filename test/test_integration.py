import os
import shutil
import uuid
from typing import *

from hypothesis import given
from hypothesis.strategies import lists, text

from LZW.__main__ import _compress, _decompress
from LZW.utils import is_equal_file

# FIXME: the testing doesn't cover the case that code dict grows beyond capacity.
MAX_FILE_LEN = 100
MAX_FILE_NUM = 3

VALID_CHARSET = [chr(i) for i in range(256)]


@given(
    l=lists(
        text(alphabet=VALID_CHARSET, max_size=MAX_FILE_LEN),
        min_size=1,
        max_size=MAX_FILE_NUM,
    )
)
def test_integration(l: List[str], tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    test_files = [f"file{i}" for i in range(len(l))]
    for test_file, s in zip(test_files, l):
        with open(test_file, "w", encoding="utf-8", newline="") as f:
            f.write(s)

    _compress("a.lzw", test_files)

    for test_file in test_files:
        shutil.move(test_file, test_file + "old")

    _decompress("a.lzw")

    for test_file in test_files:
        assert is_equal_file(test_file, test_file + "old", encoding="utf-8", newline="")
