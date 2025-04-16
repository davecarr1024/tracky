from typing import Optional, override

from tracky.core import Validatable
from tracky.track.grid.direction import Direction
from tracky.track.grid.position import Position


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
        if reverse_piece := self.reverse_piece:
            return reverse_piece.connection(-self.reverse_direction)

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

    @override
    def _validate(self) -> None:
        if (piece_ := self.piece) and (self not in piece_.connections):
            raise self._validation_error(f"connection {self} not in piece {piece_}")


from tracky.track.grid import grid as grid_lib
from tracky.track.pieces import piece
