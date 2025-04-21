import math
from typing import SupportsFloat, Union, overload, override

from tracky.track import Direction


class Rotation:
    """Screen space rotation.

    Normalized to be in the range [-pi, pi].
    """

    @staticmethod
    def _normalize(th: float) -> float:
        return (th + math.pi * 3) % (math.pi * 2) - math.pi

    def __init__(self, radians: SupportsFloat) -> None:
        self.__th = self._normalize(float(radians))

    @override
    def __repr__(self) -> str:
        return f"Rotation({self.degrees})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Rotation) and abs(self.radians - other.radians) < 1e-5

    @property
    def degrees(self) -> float:
        return math.degrees(self.__th)

    @property
    def radians(self) -> float:
        return self.__th

    @classmethod
    def from_degrees(cls, degrees: SupportsFloat) -> "Rotation":
        return cls(math.radians(degrees))

    @classmethod
    def from_radians(cls, radians: SupportsFloat) -> "Rotation":
        return cls(radians)

    def __neg__(self) -> "Rotation":
        return Rotation(-self.radians)

    def __add__(self, rhs: "Rotation") -> "Rotation":
        return Rotation(self.radians + rhs.radians)

    def __sub__(self, rhs: "Rotation") -> "Rotation":
        return Rotation(self.radians - rhs.radians)

    @overload
    def __mul__(self, rhs: SupportsFloat) -> "Rotation": ...

    @overload
    def __mul__(self, rhs: "offset.Offset") -> "offset.Offset": ...

    def __mul__(
        self, rhs: Union[SupportsFloat, "offset.Offset"]
    ) -> Union["Rotation", "offset.Offset"]:
        match rhs:
            case SupportsFloat():
                return Rotation(self.radians * float(rhs))
            case offset.Offset():
                th = (rhs.as_rotation() + self).radians
                return offset.Offset(int(math.cos(th) * rhs.length), int(math.sin(th) * rhs.length))

    def lerp(self, rhs: "Rotation", u: SupportsFloat) -> "Rotation":
        return self + (rhs - self) * u

    @classmethod
    def from_direction(cls, direction: Direction) -> "Rotation":
        match direction:
            case Direction.UP:
                return cls.from_degrees(-90)
            case Direction.RIGHT:
                return cls.from_degrees(0)
            case Direction.DOWN:
                return cls.from_degrees(90)
            case Direction.LEFT:
                return cls.from_degrees(-180)


from tracky.visuals import offset
