import os
import uuid

from hypothesis import given
from hypothesis.strategies import text

from LZW.iostream import FileInStreamer

# TODO: test read in binary mode


@given(s=text())
def test_file_in_streamer(s: str, tmp_path) -> None:
    # We need to intentionally create a unique subpath for each function invocation
    # Because every hypothesis' example of the test function share the same
    # tmp_path fixture instance, which is undesirable for some test cases.
    subpath = tmp_path / str(uuid.uuid4())
    subpath.mkdir()
    os.chdir(subpath)

    filename = "temp.txt"
    with open(filename, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    fs = FileInStreamer(filename, encoding="utf-8", newline="")
    assert list(fs) == list(s)


# TODO: test write_to_file_from_stream
