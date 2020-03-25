from typing import AnyStr, Iterable, Iterator


class FileInStreamer:
    """ A simple and thin stream wrapper of file content, read in one byte at a time """

    def __init__(self, filename: str, mode: str = "r", **kwargs) -> None:
        # self._context_manager = open(filename, mode, **kwargs)
        # self._fp = self._context_manager.__enter__()
        self._fp = open(filename, mode, **kwargs)

    __slots__ = ("_fp",)

    def __next__(self) -> AnyStr:
        byte = self._fp.read(1)
        if byte:
            return byte
        else:
            raise StopIteration

    def __iter__(self) -> Iterator:
        return self

    def __del__(self) -> None:
        # self._context_manager.__exit__(None, None, None)
        self._fp.close()


def write_to_file_from_stream(
    sstream: Iterable[AnyStr], filename: str, mode: str = "w", **kwargs
) -> None:
    with open(filename, mode, **kwargs) as f:
        for s in sstream:
            f.write(s)


class FileOutStreamer:
    pass