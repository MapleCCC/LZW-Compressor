import os
from tempfile import TemporaryDirectory

from hypothesis import given
from hypothesis.strategies import integers

from codec import *
from utils import generate_gibberish, generate_gibberish_file, is_equal_file, isplit

MAX_FILE_LEN = 100

# VALID_CHARSET = (string.ascii_letters + string.digits + string.punctuation + string.whitespace)
VALID_CHARSET = [chr(i) for i in range(256)]


@given(integers(min_value=0, max_value=MAX_FILE_LEN))
def test_encode_decode(text_len: int) -> None:
    random_text = generate_gibberish(text_len, charset=VALID_CHARSET)
    assert "".join(lzw_decode(lzw_encode(random_text, 12), 12)) == random_text


@given(integers(min_value=0, max_value=MAX_FILE_LEN))
def test_encode_decode_file(text_len: int) -> None:
    code_bit = 12
    VIRTUAL_EOF = 2 ** code_bit - 1
    # with TemporaryDirectory() as directory:
        # os.chdir(directory)
    original_filename = "file0"
    decoded_filename = "file0_decoded"
    random_text = generate_gibberish(text_len, charset=VALID_CHARSET)
    with open(original_filename, "w", encoding="utf-8", newline="") as f:
        f.write(random_text)
    codes = encode_file(original_filename, code_size=code_bit)
    codes = isplit(codes, VIRTUAL_EOF).__next__()
    decode_file(decoded_filename, codes, code_size=code_bit)
    assert is_equal_file(original_filename, decoded_filename)
