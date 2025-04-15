from typing import Optional, override

from tracky.core import Validatable
from tracky.track.grid.direction import Direction
from tracky.track.grid.position import Position


class Connection(Validatable):
    def __init__(
        self,
        from_direction: Direction,
        to_direction: Direction,
        piece: Optional["piece.Piece"] = None,
    ) -> None:
        super().__init__()
        self.__from_direction = from_direction
        self.__to_direction = to_direction
        self.__piece: Optional["piece.Piece"] = None
        with self._pause_validation():
            self.piece = piece

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @property
    def from_direction(self) -> Direction:
        return self.__from_direction

    @property
    def from_position(self) -> Optional["Position"]:
        if piece_ := self.piece:
            return piece_.position + self.from_direction

    @property
    def from_piece(self) -> Optional["piece.Piece"]:
        if (
            (piece_ := self.piece)
            and (grid := piece_.grid)
            and (from_position := self.from_position)
        ):
            return grid.get(from_position)

    @property
    def to_direction(self) -> Direction:
        return self.__to_direction

    @property
    def to_position(self) -> Optional["Position"]:
        if piece_ := self.piece:
            return piece_.position + self.to_direction

    @property
    def to_piece(self) -> Optional["piece.Piece"]:
        if (
            (piece_ := self.piece)
            and (grid := piece_.grid)
            and (to_position := self.to_position)
        ):
            return grid.get(to_position)

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

    @override
    def _validate(self) -> None:
        if (piece_ := self.piece) and (self not in piece_.connections):
            raise self._validation_error(f"connection {self} not in piece {piece_}")


from tracky.track.piece import piece
