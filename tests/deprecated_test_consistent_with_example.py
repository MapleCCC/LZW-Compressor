import os
import subprocess
import uuid
from pathlib import Path
from random import sample
from typing import List

from hypothesis import given, settings, example
from hypothesis.strategies import binary, lists

from LZW.__main__ import lzw_compress, lzw_decompress

EXAMPLE_EXE = os.path.join(os.getcwd(), "lzw_example_win.exe")

MAX_TEST_FILE_LEN = 10000
MAX_NUM_TEST_FILES = 10


TEST_FILES_BUILD_STRATEGY = lists(
    # lzw_example_win.exe is not able to handle empty input files
    binary(min_size=1, max_size=MAX_TEST_FILE_LEN),
    # lzw_example_win.exe is not able to handle zero input files
    min_size=1,
    max_size=MAX_NUM_TEST_FILES,
)


# TODO: add test case for code dict overflow
# All possible one-length bytes
VALID_CHARSET = [i.to_bytes(1, "big") for i in range(256)]
EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW = b"".join(
    b"".join(sample(VALID_CHARSET, k=256)) for _ in range(20)
)


@given(l=TEST_FILES_BUILD_STRATEGY)
@example(l=[EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW] * MAX_NUM_TEST_FILES)
@settings(deadline=None)
def test_compression(l: List[bytes], tmp_path: Path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    test_files = [Path(f"file{i}") for i in range(len(l))]
    for test_file, s in zip(test_files, l):
        test_file.write_bytes(s)

    subprocess.run(
        [EXAMPLE_EXE, "-c", "a.lzw"] + [str(x) for x in test_files]
    ).check_returncode()

    for test_file in test_files:
        test_file.unlink()

    lzw_decompress("a.lzw")

    for test_file, s in zip(test_files, l):
        assert test_file.read_bytes() == s


@given(l=TEST_FILES_BUILD_STRATEGY)
@example(l=[EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW] * 3)
@settings(deadline=None)
def test_decompression(l: List[bytes], tmp_path: Path) -> None:
    # def test_decompression(tmp_path) -> None:
    # l = [b"", b"\x00\x00"]
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    test_files = [Path(f"file{i}") for i in range(len(l))]
    for test_file, s in zip(test_files, l):
        test_file.write_bytes(s)

    lzw_compress("a.lzw", [str(x) for x in test_files])

    for test_file in test_files:
        test_file.unlink()

    subprocess.run([EXAMPLE_EXE, "-d", "a.lzw"]).check_returncode()

    for test_file, s in zip(test_files, l):
        assert test_file.read_bytes() == s
