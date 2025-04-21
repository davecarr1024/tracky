from dataclasses import dataclass

from tracky.core import Error, Errorable
from tracky.visuals.offset import Offset
from tracky.visuals.position import Position


@dataclass(frozen=True)
class Rectangle(Errorable):
    class ValueError(Error, ValueError): ...

    min: Position
    max: Position

    def __post_init__(self) -> None:
        if self.min.x > self.max.x or self.min.y > self.max.y:
            raise self._error(f"invalid rect bounds {self.min} > {self.max}", self.ValueError)

    @property
    def size(self) -> Offset:
        return self.max - self.min

    @property
    def width(self) -> int:
        return self.size.dx

    @property
    def height(self) -> int:
        return self.size.dy

    def __contains__(self, rhs: Position) -> bool:
        return self.min.x <= rhs.x < self.max.x and self.min.y <= rhs.y < self.max.y
