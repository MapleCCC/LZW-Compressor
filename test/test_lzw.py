import os
import random
import string
import subprocess
from tempfile import TemporaryDirectory

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from lzw.codec import lzw_decode, lzw_encode
from lzw.utils import *

MAX_NUM_TEST_FILES = 10

EXAMPLE_EXE = os.path.join(os.getcwd(), "lzw_example_win.exe")
BASELINE_EXE = os.path.join(os.getcwd(), "baseline.py")
EXPERIMENT_EXE = os.path.join(os.getcwd(), "lzw.exe")


def test_regression() -> None:
    text = read_file_content("Ephesians.txt")
    assert lzw_decode(lzw_encode(text)) == text
    text = read_file_content("Matthew.txt")
    assert lzw_decode(lzw_encode(text)) == text


# @given(integers(min_value=0, max_value=MAX_FILE_LEN))
# def test_encode_decode_file(text_len: int) -> None:
def test_encode_decode_file() -> None:
    text_len = 0

    with TemporaryDirectory() as directory:
        os.chdir(directory)

        test_files = [
            f"file{i}" for i in range(random.randrange(1, MAX_NUM_TEST_FILES))
        ]
        for test_file in test_files:
            generate_gibberish_file(test_file, text_len)

        subprocess.run(
            ["python", BASELINE_EXE, "compress", "output_baseline.lzw"] + test_files
        )

        for file in test_files:
            os.rename(file, file + ".bak")

        subprocess.run(["python", BASELINE_EXE, "decompress", "output_baseline.lzw"])

        # print(subprocess.getoutput("ls"))

        # for file in test_files:
        #     assert diff_file(file, file + ".bak", newline="")


# There are different testing strategies. Our easy way is to set the random seed.
@pytest.mark.skip(reason="Not Yet Implemented")
@given(integers())
def test_compression(seed: int) -> None:
    random.seed(seed)

    with TemporaryDirectory() as directory:
        os.chdir(directory)

        test_files = [
            f"file{i}" for i in range(random.randrange(1, MAX_NUM_TEST_FILES))
        ]
        for test_file in test_files:
            generate_gibberish_file(test_file)

        subprocess.run([EXAMPLE_EXE, "-c", "output_example.lzw"] + test_files)
        # subprocess.run([EXPERIMENT_EXE, "-c", "output.lzw"] + test_files)
        subprocess.run(
            ["python", BASELINE_EXE, "compress", "output_baseline.lzw"] + test_files
        )

        assert diff_file("output_baseline.lzw", "output_example.lzw", is_binary=True)


@pytest.mark.skip(reason="Not Yet Implemented")
def test_decompress():
    raise NotImplementedError
