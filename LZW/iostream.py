from typing import Any, AnyStr, Iterable, Iterator


class FileInStreamer:
    """ A simple and thin stream wrapper of file content, read in one byte at a time """

    def __init__(self, filename: AnyStr, mode: str = "r", **kwargs: Any) -> None:
        # self._context_manager = open(filename, mode, **kwargs)
        # self._fp = self._context_manager.__enter__()
        self._fp = open(filename, mode, **kwargs)

    __slots__ = ("_fp",)

    def __next__(self) -> AnyStr:
        byte = self._fp.read(1)
        if byte:
            return byte
        else:
            self._fp.close()
            raise StopIteration

    def __iter__(self) -> Iterator:
        return self


def write_to_file_from_stream(
    sstream: Iterable[AnyStr], filename: AnyStr, mode: str = "w", **kwargs: Any
) -> None:
    with open(filename, mode, **kwargs) as f:
        for s in sstream:
            f.write(s)


class FileOutStreamer:
    pass
