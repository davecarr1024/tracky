from typing import override

import pytest

from tracky.core.error import Error
from tracky.core.errorable import Errorable


class _Errorable(Errorable):
    class ValueError(Error): ...

    def __init__(self, name: str) -> None:
        self.name = name

    @override
    def __str__(self) -> str:
        return self.name

    def set(self, value: int) -> int:
        if value < 0:
            raise self._error("value must be non-negative", self.ValueError)
        return value

    def try_set(self, value: int) -> int:
        return self._try(lambda: self.set(value), "set failed", self.ValueError)


def test_throw() -> None:
    e = _Errorable("test")
    with pytest.raises(_Errorable.ValueError) as excinfo:
        e.set(-1)
    assert str(excinfo.value) == "test: value must be non-negative"


def test_try_success() -> None:
    e = _Errorable("test")
    assert e.try_set(1) == 1


def test_try_fail() -> None:
    e = _Errorable("test")
    with pytest.raises(_Errorable.ValueError) as excinfo:
        e.try_set(-1)
    assert str(excinfo.value) == "test: set failed"
