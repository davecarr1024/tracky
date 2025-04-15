from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator, final

from tracky.core.error import Error
from tracky.core.errorable import Errorable


class Validatable(ABC, Errorable):
    class ValidationError(Error): ...

    def __init__(self) -> None:
        self.__pause_validation_count = 0

    @final
    @property
    def _validation_enabled(self) -> bool:
        return self.__pause_validation_count == 0

    @final
    @contextmanager
    def _pause_validation(self) -> Iterator[None]:
        try:
            self.__pause_validation_count += 1
            yield
        finally:
            self.__pause_validation_count -= 1
            self._validate_if_enabled()

    @final
    def _validate_if_enabled(self) -> None:
        if self._validation_enabled:
            self._validate()

    def _validation_error(self, message: str) -> "Validatable.ValidationError":
        return self._error(message, self.ValidationError)

    @abstractmethod
    def _validate(self) -> None: ...
