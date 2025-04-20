from dataclasses import dataclass

from tracky.core import Error, Errorable


@dataclass(frozen=True)
class Rotation(Errorable):
    """A grid rotation class that holds a number of clockwise rotations."""

    class ValueError(Error, ValueError): ...

    n: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "n", self.n % 4)

    def __neg__(self) -> "Rotation":
        return Rotation(-self.n)

    def __add__(self, rhs: "Rotation") -> "Rotation":
        return Rotation(self.n + rhs.n)

    def __sub__(self, rhs: "Rotation") -> "Rotation":
        return Rotation(self.n - rhs.n)

    def __mul__(self, rhs: "direction.Direction") -> "direction.Direction":
        result = rhs
        for _ in range(self.n % 4):
            match result:
                case direction.Direction.LEFT:
                    result = direction.Direction.UP
                case direction.Direction.UP:
                    result = direction.Direction.RIGHT
                case direction.Direction.RIGHT:
                    result = direction.Direction.DOWN
                case direction.Direction.DOWN:
                    result = direction.Direction.LEFT
        return result

    def __rmul__(self, lhs: "direction.Direction") -> "direction.Direction":
        return self.__mul__(lhs)


from tracky.track.grid import direction
