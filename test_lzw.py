import os
import random
import string
import subprocess
from tempfile import TemporaryDirectory

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from baseline import lzw_decode, lzw_encode
from utils import *

VALID_CHARSET = (
    string.ascii_letters + string.digits + string.punctuation + string.whitespace
)

MAX_FILE_LEN = 7000
MAX_NUM_TEST_FILES = 10

EXAMPLE_EXE = os.path.join(os.getcwd(), "lzw_example_win.exe")
BASELINE_EXE = os.path.join(os.getcwd(), "baseline.py")
EXPERIMENT_EXE = os.path.join(os.getcwd(), "lzw.exe")


def generate_gibberish() -> str:
    return "".join(random.choices(VALID_CHARSET, k=random.randrange(MAX_FILE_LEN)))


def generate_gibberish_file(filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generate_gibberish())


def test_regression() -> None:
    text = read_file_content("Ephesians.txt")
    assert lzw_decode(lzw_encode(text)) == text
    text = read_file_content("Matthew.txt")
    assert lzw_decode(lzw_encode(text)) == text


@given(integers())
def test_encode_decode(seed: int) -> None:
    random.seed(seed)
    random_text = generate_gibberish()
    assert lzw_decode(lzw_encode(random_text)) == random_text


# There are different testing strategies. Our easy way is to set the random seed.
# @pytest.mark.skip(reason="Not Yet Implemented")
@given(integers())
def test_compression(seed: int) -> None:
    random.seed(seed)

    with TemporaryDirectory() as directory:
        os.chdir(directory)

        test_files = [f"file{i}" for i in range(random.randrange(MAX_NUM_TEST_FILES))]
        for test_file in test_files:
            generate_gibberish_file(test_file)

        subprocess.run([EXAMPLE_EXE, "-c", "output_example.lzw"] + test_files)
        # subprocess.run([EXPERIMENT_EXE, "-c", "output.lzw"] + test_files)
        subprocess.run([BASELINE_EXE, "compress", "output_baseline.lzw"] + test_files)

        assert diff_file("output_baseline.lzw", "output_example.lzw")


@pytest.mark.skip(reason="Not Yet Implemented")
def test_decompress():
    raise NotImplementedError
