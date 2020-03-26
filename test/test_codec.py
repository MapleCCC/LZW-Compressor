import os
import uuid

from hypothesis import given
from hypothesis.strategies import text

from LZW.codec import decode_file, encode_file, lzw_decode, lzw_encode
from LZW.utils import is_equal_file

MAX_FILE_LEN = 10000

# VALID_CHARSET = (string.ascii_letters + string.digits + string.punctuation + string.whitespace)
VALID_CHARSET = [chr(i) for i in range(256)]


@given(text(alphabet=VALID_CHARSET, max_size=MAX_FILE_LEN))
def test_encode_decode(text: str) -> None:
    assert "".join(lzw_decode(lzw_encode(text, 12), 12)) == text


@given(s=text(alphabet=VALID_CHARSET, max_size=MAX_FILE_LEN))
def test_encode_decode_file(s: str, tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    code_bit = 12

    original_filename = "file0"
    decoded_filename = "file0_decoded"

    with open(original_filename, "w", encoding="utf-8", newline="") as f:
        f.write(s)

    codes = encode_file(original_filename, code_size=code_bit)
    decode_file(decoded_filename, codes, code_size=code_bit)
    assert is_equal_file(
        original_filename, decoded_filename, encoding="utf-8", newline=""
    )
