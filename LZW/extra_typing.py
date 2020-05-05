from os import PathLike
from typing import Union

# This type hint is extracted from builtin open function's type annotation
# Except int type, we don't include.
Filename = Union[str, bytes, PathLike]
