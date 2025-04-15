from typing import override

import pytest

from tracky.core.validatable import Validatable


class _Validatable(Validatable):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.__valid = True

    @property
    def valid(self) -> bool:
        return self.__valid

    @valid.setter
    def valid(self, value: bool) -> None:
        with self._pause_validation():
            self.__valid = value

    @override
    def _validate(self) -> None:
        if not self.valid:
            raise self._validation_error("invalid")

    @override
    def __str__(self) -> str:
        return self.name

    def valid_operation(self) -> None:
        with self._pause_validation():
            self.valid = False
            self.valid = True

    def invalid_operation(self) -> None:
        self.valid = False


def test_valid_operation() -> None:
    v = _Validatable("test")
    v.valid_operation()


def test_invalid_operation() -> None:
    v = _Validatable("test")
    with pytest.raises(_Validatable.ValidationError) as excinfo:
        v.invalid_operation()
    assert str(excinfo.value) == "test: invalid"
