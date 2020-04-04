import pytest
from hypothesis import given
from hypothesis.strategies import integers

from LZW.code_dict import CodeDict


@pytest.mark.skip()
@given()
def test_get_item() -> None:
    raise NotImplementedError
