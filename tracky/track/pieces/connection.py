from typing import Optional, override

from tracky.core import Validatable
from tracky.track.grid.direction import Direction
from tracky.track.grid.position import Position
from tracky.track.grid.rotation import Rotation
from tracky.track.pieces.connection_shape import ConnectionShape


class Connection(Validatable):
    def __init__(
        self,
        reverse_direction: Direction,
        forward_direction: Direction,
        piece: Optional["piece.Piece"] = None,
    ) -> None:
        super().__init__()
        self.__reverse_direction = reverse_direction
        self.__forward_direction = forward_direction
        self.__piece: Optional["piece.Piece"] = None
        with self._pause_validation():
            self.piece = piece

    @override
    def __repr__(self) -> str:
        return (
            f"Connection(reverse_direction={self.reverse_direction}, "
            f"forward_direction={self.forward_direction}, "
            f"position={self.piece.position if self.piece else None})"
        )

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @property
    def reverse_direction(self) -> Direction:
        return self.__reverse_direction

    @property
    def reverse_position(self) -> Optional[Position]:
        if position := self.position:
            return position + self.reverse_direction

    def _piece(self, position: Optional[Position]) -> Optional["piece.Piece"]:
        if position and (grid := self.grid):
            return grid.get(position)

    @property
    def reverse_piece(self) -> Optional["piece.Piece"]:
        return self._piece(self.reverse_position)

    @property
    def reverse_connection(self) -> Optional["Connection"]:
        """Get the connection for reversing from this connection.

        Note that this isn't necessarily the connection that got you to this connection.
        Consider a trailing switch with connections LEFT-RIGHT UP-RIGHT and RIGHT-UP. You
        traverse that switch going LEFT-RIGHT and get one piece beyond, then back up u=1.
        You'll end up on the RIGHT-UP connection even though you didn't come from there.

        Note that this preserves directionality. You aren't going backwards the other way.
        You want to end up on a connection that has the same direction as the one you're
        currently pointed in.
        """
        # Get the piece we came from, always the same.
        if reverse_piece := self.reverse_piece:
            # Get the connection we would go over if we were going the opposite
            # direction.
            if incoming_connection := reverse_piece.connections_by_direction.get(
                -self.reverse_direction
            ):
                # Get the complimentary connection to that, which is the connection we
                # would end up on if we were going backwards. Note that this doesn't
                # have to exist. Some pieces can be directional, like a derailer or a
                # signal. That's ok and representable.
                return reverse_piece.connections_by_direction.get(
                    incoming_connection.forward_direction
                )

    @property
    def forward_direction(self) -> Direction:
        return self.__forward_direction

    @property
    def forward_position(self) -> Optional["Position"]:
        if position := self.position:
            return position + self.forward_direction

    @property
    def forward_piece(self) -> Optional["piece.Piece"]:
        return self._piece(self.forward_position)

    @property
    def forward_connection(self) -> Optional["Connection"]:
        if forward_piece := self.forward_piece:
            return forward_piece.connection(-self.forward_direction)

    @property
    def piece(self) -> Optional["piece.Piece"]:
        return self.__piece

    @piece.setter
    def piece(self, piece: Optional["piece.Piece"]) -> None:
        if piece is not self.__piece:
            with self._pause_validation():
                if self.__piece is not None:
                    self.__piece.remove_connection(self)
                self.__piece = piece
                if self.__piece is not None:
                    self.__piece.add_connection(self)

    @property
    def grid(self) -> Optional["grid_lib.Grid"]:
        if piece_ := self.piece:
            return piece_.grid

    @property
    def position(self) -> Optional["Position"]:
        if piece_ := self.piece:
            return piece_.position

    @property
    def connection_shape(self) -> Optional["ConnectionShape"]:
        if piece_ := self.piece:
            return piece_.connection_shape

    @override
    def _validate(self) -> None:
        if (piece_ := self.piece) and (self not in piece_.connections):
            raise self._validation_error(f"connection {self} not in piece {piece_}")

    def rotate(self, rotation: Rotation) -> "Connection":
        return Connection(
            reverse_direction=self.reverse_direction * rotation,
            forward_direction=self.forward_direction * rotation,
        )

    def is_same_as(self, rhs: "Connection") -> bool:
        return (
            self.reverse_direction == rhs.reverse_direction
            and self.forward_direction == rhs.forward_direction
        )

    def rotation_to(self, rhs: "Connection") -> Optional[Rotation]:
        for i in range(4):
            rotation = Rotation(i)
            if self.rotate(rotation).is_same_as(rhs):
                return rotation


from tracky.track.grid import grid as grid_lib
from tracky.track.pieces import piece
