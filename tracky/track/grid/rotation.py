from dataclasses import dataclass

from tracky.core import Error, Errorable


@dataclass(frozen=True)
class Rotation(Errorable):
    """A grid rotation class that holds a number of clockwise rotations."""

    class ValueError(Error, ValueError): ...

    n: int

    def __neg__(self) -> "Rotation":
        return Rotation(-self.n)

    def __mul__(self, rhs: "direction.Direction") -> "direction.Direction":
        result = rhs
        for _ in range(self.n % 4):
            match result:
                case direction.LEFT:
                    result = direction.UP
                case direction.UP:
                    result = direction.RIGHT
                case direction.RIGHT:
                    result = direction.DOWN
                case direction.DOWN:
                    result = direction.LEFT
                case _:
                    raise self._error(f"invalid direction {direction}", self.ValueError)
        return result

    def __rmul__(self, lhs: "direction.Direction") -> "direction.Direction":
        return self.__mul__(lhs)


from tracky.track.grid import direction
