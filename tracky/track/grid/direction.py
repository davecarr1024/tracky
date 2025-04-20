from enum import Enum

from tracky.core import Errorable


class Direction(Errorable, Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, drow: int, dcol: int):
        self.drow = drow
        self.dcol = dcol

    def __neg__(self) -> "Direction":
        match self:
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.UP:
                return Direction.DOWN
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.DOWN:
                return Direction.UP
