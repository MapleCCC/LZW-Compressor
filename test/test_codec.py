import os
import uuid
from random import sample

from hypothesis import example, given, settings
from hypothesis.strategies import binary

from LZW.codec import LZWDecoder, LZWEncoder
from LZW.pep467 import iterbytes
from LZW.utils import ascii2byte, is_equal_file

MAX_FILE_LEN = 10000
CODE_BIT = 12

# All possible one-length bytes
VALID_CHARSET = [ascii2byte(i) for i in range(256)]

EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW = b"".join(
    b"".join(sample(VALID_CHARSET, k=256)) for _ in range(20)
)


@given(s=binary(max_size=MAX_FILE_LEN))
@example(s=EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW)
@settings(deadline=None)
def test_encode_decode(s: bytes) -> None:
    encoder = LZWEncoder(CODE_BIT)
    decoder = LZWDecoder(CODE_BIT)
    assert b"".join(decoder._decode(encoder._encode(iterbytes(s)))) == s


@given(s=binary(max_size=MAX_FILE_LEN))
def test_encode_decode_file(s: bytes, tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    original_filename = "file0"
    decoded_filename = "file0_decoded"

    with open(original_filename, "wb") as f:
        f.write(s)

    encoder = LZWEncoder(code_size=CODE_BIT)
    decoder = LZWDecoder(code_size=CODE_BIT)
    codes = encoder.encode_file(original_filename)
    decoder.decode_file(decoded_filename, codes)
    assert is_equal_file(original_filename, decoded_filename, mode="rb")
