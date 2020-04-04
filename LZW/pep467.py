from typing import Iterator


# Reference: https://www.python.org/dev/peps/pep-0467/#addition-of-getbyte-method-to-retrieve-a-single-byte
def getbyte(bs: bytes, index: int) -> bytes:
    try:
        return bs[index].to_bytes(1, "big")
    except IndexError:
        raise IndexError("index out of range")


# Reference: https://www.python.org/dev/peps/pep-0467/#addition-of-optimised-iterator-methods-that-produce-bytes-objects
def iterbytes(bs: bytes) -> Iterator[bytes]:
    """
    Iterate through bytes object and emit 1-length
    bytes each time, instead of int.
    """
    for b in bs:
        assert isinstance(b, int)
        yield b.to_bytes(1, "big")
