from dataclasses import dataclass

from tracky.core import Error, Errorable
from tracky.visuals.vector import Vector


@dataclass(frozen=True)
class Rectangle(Errorable):
    class ValueError(Error, ValueError): ...

    min: Vector
    max: Vector

    def __post_init__(self) -> None:
        if self.min > self.max:
            raise self._error(f"invalid rect bounds {self.min} > {self.max}", self.ValueError)

    @property
    def size(self) -> Vector:
        return self.max - self.min

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def __contains__(self, rhs: Vector) -> bool:
        return rhs >= self.min and rhs <= self.max
