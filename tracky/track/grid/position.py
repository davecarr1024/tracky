from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, direction_: "direction.Direction") -> "Position":
        return Position(self.row + direction_.drow, self.col + direction_.dcol)

    def __sub__(self, direction_: "direction.Direction") -> "Position":
        return self + (-direction_)


from tracky.track.grid import direction
