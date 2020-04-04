import functools
import os
import uuid

from hypothesis import given
from hypothesis.strategies import text

from LZW.utils import *


@given(s=text(), t=text())
def test_is_equal_file(s: str, t: str, tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    file1 = "temp1.txt"
    file2 = "temp2.txt"

    open(file1, "w", encoding="utf-8", newline="").write(s)
    open(file2, "w", encoding="utf-8", newline="").write(s)

    assert is_equal_file(file1, file2, encoding="utf-8", newline="")

    open(file1, "w", encoding="utf-8", newline="").write(s)
    if s == t:
        t += "1"
    open(file2, "w", encoding="utf-8", newline="").write(t)

    assert not is_equal_file(file1, file2, encoding="utf-8", newline="")


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
