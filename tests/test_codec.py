import os
import uuid
from pathlib import Path
from random import sample

from hypothesis import example, given, settings
from hypothesis.strategies import binary

from LZW.codec import LZWDecoder, LZWEncoder
from LZW.pep467 import iterbytes

MAX_FILE_LEN = 10000
CODE_BITSIZE = 12

# All possible one-length bytes
VALID_CHARSET = [i.to_bytes(1, "big") for i in range(256)]

EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW = b"".join(
    b"".join(sample(VALID_CHARSET, k=256)) for _ in range(20)
)


@given(s=binary(max_size=MAX_FILE_LEN))
@example(s=EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW)
@settings(deadline=None)
def test_encode_decode(s: bytes) -> None:
    encoder = LZWEncoder(CODE_BITSIZE)
    decoder = LZWDecoder(CODE_BITSIZE)
    assert b"".join(decoder._decode(encoder._encode(iterbytes(s)))) == s


@given(s=binary(max_size=MAX_FILE_LEN))
@example(s=EXAMPLE_TEXT_TEST_CODE_DICT_OVERFLOW)
@settings(deadline=None)
def test_encode_decode_file(s: bytes, tmp_path: Path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    original_file = Path("file0")
    decoded_file = Path("file0_decoded")

    original_file.write_bytes(s)

    encoder = LZWEncoder(CODE_BITSIZE)
    decoder = LZWDecoder(CODE_BITSIZE)
    codes = encoder.encode_file(str(original_file))
    decoder.decode_file(str(decoded_file), codes)
    assert original_file.read_bytes() == decoded_file.read_bytes()
