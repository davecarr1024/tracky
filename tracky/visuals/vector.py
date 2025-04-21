import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    """Screen-space pixel position."""

    x: int
    y: int

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __add__(self, rhs: "Vector") -> "Vector":
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs: "Vector") -> "Vector":
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, rhs: int | float) -> "Vector":
        return Vector(int(self.x * rhs), int(self.y * rhs))

    def __floordiv__(self, rhs: int | float) -> "Vector":
        return Vector(int(self.x // rhs), int(self.y // rhs))

    def __lt__(self, rhs: "Vector") -> bool:
        return self.x < rhs.x and self.y < rhs.y

    def __le__(self, rhs: "Vector") -> bool:
        return self.x <= rhs.x and self.y <= rhs.y

    def __gt__(self, rhs: "Vector") -> bool:
        return self.x > rhs.x and self.y > rhs.y

    def __ge__(self, rhs: "Vector") -> bool:
        return self.x >= rhs.x and self.y >= rhs.y

    def lerp(self, rhs: "Vector", u: float) -> "Vector":
        return self + (rhs - self) * u

    @property
    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def norm(self) -> "Vector":
        return self // self.length
