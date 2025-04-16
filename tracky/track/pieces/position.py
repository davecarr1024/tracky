from dataclasses import dataclass
from typing import Optional

from tracky.core import Error, Errorable
from tracky.track.pieces import Connection, Piece


@dataclass(frozen=True)
class Position(Errorable):
    class ValueError(Error, ValueError): ...

    connection: Connection
    u: float

    def __add__(self, du: float) -> "Position":
        print(f"adding {du} to {self}")
        u = self.u + du
        if u > 1:
            print(f"u > 1: {u}")
            u -= 1
            print(f"u -= 1: {u}")
            if (forward_connection := self.connection.forward_connection) is None:
                raise self._error("no forward connection", self.ValueError)
            print(f"forward connection: {forward_connection}")
            return Position(forward_connection, u)
        elif u < 0:
            print(f"u < 0: {u}")
            u += 1
            print(f"u += 1: {u}")
            if (reverse_connection := self.connection.reverse_connection) is None:
                raise self._error("no reverse connection", self.ValueError)
            return Position(reverse_connection, u)
        else:
            return Position(self.connection, u)

    def __sub__(self, du: float) -> "Position":
        return self + (-du)

    @property
    def piece(self) -> Optional[Piece]:
        return self.connection.piece

    @property
    def grid_position(self) -> Optional["grid_position.Position"]:
        if piece := self.piece:
            return piece.position

    @property
    def grid(self) -> Optional["grid.Grid"]:
        if piece := self.piece:
            return piece.grid


from tracky.track.grid import grid
from tracky.track.grid import position as grid_position
