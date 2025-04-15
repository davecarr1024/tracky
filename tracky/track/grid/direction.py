from dataclasses import dataclass

from tracky.core.error import Error


@dataclass(frozen=True)
class Direction:
    class Error(Error): ...

    class ValueError(Error, ValueError): ...

    drow: int
    dcol: int

    def __str__(self) -> str:
        match (self.drow, self.dcol):
            case (0, 1):
                return "RIGHT"
            case (0, -1):
                return "LEFT"
            case (1, 0):
                return "DOWN"
            case (-1, 0):
                return "UP"
            case _:
                raise self.ValueError(f"Invalid direction: {self.drow}, {self.dcol}")

    def __post_init__(self) -> None:
        if (self.drow, self.dcol) not in (
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ):
            raise self.ValueError(f"Invalid direction: {self.drow}, {self.dcol}")

    def __neg__(self) -> "Direction":
        return Direction(-self.drow, -self.dcol)


UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)
