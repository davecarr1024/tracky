from dataclasses import dataclass
from typing import SupportsFloat, Union, overload


@dataclass(frozen=True)
class Position:
    """Screen-space pixel position."""

    x: int
    y: int

    def __add__(self, rhs: "offset.Offset") -> "Position":
        return Position(self.x + rhs.dx, self.y + rhs.dy)

    @overload
    def __sub__(self, rhs: "Position") -> "offset.Offset": ...

    @overload
    def __sub__(self, rhs: "offset.Offset") -> "Position": ...

    def __sub__(
        self, rhs: Union["Position", "offset.Offset"]
    ) -> Union["offset.Offset", "Position"]:
        match rhs:
            case Position():
                return offset.Offset(self.x - rhs.x, self.y - rhs.y)
            case offset.Offset():
                return Position(self.x - rhs.dx, self.y - rhs.dy)

    def lerp(self, rhs: "Position", u: SupportsFloat) -> "Position":
        return self + (rhs - self) * u

    def direction_to(self, rhs: "Position") -> "rotation.Rotation":
        """Get the direction from self to rhs.

        Note that this is in screen space, so it is the direction that points from self to rhs.
        It isn't a rotation of self as an offset to yield rhs.
        """
        return (rhs - self).as_rotation()


from tracky.visuals import offset, rotation
