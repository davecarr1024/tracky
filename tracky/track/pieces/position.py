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
        connection = self.connection
        u = self.u + du
        print(f"moving {du} from {self.u} to {u} at {connection}")
        while u >= 1:
            print(f"moving forward from {u} at {connection}")
            u -= 1
            if (forward_connection := connection.forward_connection) is None:
                raise self._error("no forward connection", self.ValueError)
            connection = forward_connection
            print(f"moved forward to {u} at {connection}")
        while u < 0:
            print(f"moving backward from {u} at {connection}")
            u += 1
            if (reverse_connection := connection.reverse_connection) is None:
                raise self._error("no reverse connection", self.ValueError)
            connection = reverse_connection
            print(f"moved backward to {u} at {connection}")
        print(f"moved to {u} at {connection}")
        return Position(connection, u)

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
