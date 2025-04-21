import math
from dataclasses import dataclass
from typing import SupportsFloat, Union, overload


@dataclass(frozen=True)
class Offset:
    """Offset in screen space between positions."""

    dx: int
    dy: int

    @overload
    def __add__(self, rhs: "Offset") -> "Offset": ...

    @overload
    def __add__(self, rhs: "position.Position") -> "position.Position": ...

    def __add__(
        self, rhs: Union["Offset", "position.Position"]
    ) -> Union["Offset", "position.Position"]:
        match rhs:
            case Offset():
                return Offset(self.dx + rhs.dx, self.dy + rhs.dy)
            case position.Position():
                return position.Position(rhs.x + self.dx, rhs.y + self.dy)

    def __neg__(self) -> "Offset":
        return Offset(-self.dx, -self.dy)

    def __sub__(self, rhs: "Offset") -> "Offset":
        return self + (-rhs)

    def __mul__(self, rhs: SupportsFloat) -> "Offset":
        return Offset(int(self.dx * float(rhs)), int(self.dy * float(rhs)))

    def __floordiv__(self, rhs: SupportsFloat) -> "Offset":
        return Offset(int(self.dx // float(rhs)), int(self.dy // float(rhs)))

    @property
    def length(self) -> float:
        return math.sqrt(self.dx * self.dx + self.dy * self.dy)

    def norm(self) -> "Offset":
        return self // self.length

    def as_rotation(self) -> "rotation.Rotation":
        return rotation.Rotation.from_radians(math.atan2(self.dy, self.dx))

    def lerp(self, rhs: "Offset", u: SupportsFloat) -> "Offset":
        return self + (rhs - self) * u


from tracky.visuals import position, rotation
