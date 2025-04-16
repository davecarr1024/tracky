from collections import defaultdict
from typing import Iterable, Iterator, Mapping, MutableMapping, Optional, override

from tracky.core import Error, Validatable
from tracky.track.grid.direction import DOWN, LEFT, RIGHT, UP, Direction
from tracky.track.grid.position import Position


class Grid(Validatable, MutableMapping[Position, "piece.Piece"]):
    class KeyError(Error, KeyError): ...

    def __init__(
        self,
        pieces: Optional[Iterable["piece.Piece"]] = None,
    ) -> None:
        super().__init__()
        self.__pieces = frozenset[piece.Piece]()
        with self._pause_validation():
            if pieces is not None:
                self.pieces = frozenset(pieces)

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @property
    def pieces(self) -> frozenset["piece.Piece"]:
        return self.__pieces

    @pieces.setter
    def pieces(self, pieces: Iterable["piece.Piece"]) -> None:
        pieces_ = frozenset(pieces)
        if pieces_ != self.__pieces:
            with self._pause_validation():
                added_pieces = pieces_ - self.__pieces
                removed_pieces = self.__pieces - pieces_
                self.__pieces = pieces_
                for piece in added_pieces:
                    piece.grid = self
                for piece in removed_pieces:
                    piece.grid = None

    def add_piece(self, piece: "piece.Piece") -> None:
        self.pieces = self.__pieces | {piece}

    def remove_piece(self, piece: "piece.Piece") -> None:
        self.pieces = self.__pieces - {piece}

    @override
    def _validate(self) -> None:
        for piece_ in self.__pieces:
            if piece_.grid != self:
                raise self._validation_error(f"piece {piece_} not in grid")
        pieces_by_position = defaultdict[Position, set[piece.Piece]](set)
        for piece_ in self.__pieces:
            pieces_by_position[piece_.position].add(piece_)
        for position, pieces in pieces_by_position.items():
            if len(pieces) > 1:
                raise self._validation_error(f"multiple pieces at position {position}: {pieces}")

    @property
    def pieces_by_position(self) -> Mapping[Position, "piece.Piece"]:
        return {piece.position: piece for piece in self.__pieces}

    @override
    def __len__(self) -> int:
        return len(self.__pieces)

    @override
    def __iter__(self) -> Iterator[Position]:
        return iter(self.pieces_by_position)

    @override
    def __getitem__(self, position: Position) -> "piece.Piece":
        try:
            return self.pieces_by_position[position]
        except KeyError as e:
            raise self.KeyError(f"no piece at position {position}") from e

    @override
    def __setitem__(self, position: Position, piece: "piece.Piece") -> None:
        if piece.position != position:
            raise self._validation_error(f"piece {piece} has wrong position {position}")
        self.add_piece(piece)

    @override
    def __delitem__(self, position: Position) -> None:
        self.remove_piece(self[position])

    @classmethod
    def create_loop(
        cls,
        rows: int,
        cols: int,
        start_position: Optional[Position] = None,
    ) -> "Grid":
        start_position_ = start_position if start_position is not None else Position(0, 0)
        start_row = start_position_.row
        start_col = start_position_.col
        top = start_row
        bottom = start_col + cols - 1
        left = start_col
        right = start_row + rows - 1
        return Grid(
            pieces=set[piece.Piece].union(
                {
                    piece.Piece.create(
                        Position(row, left),
                        UP,
                        DOWN,
                    )
                    for row in range(top + 1, bottom)
                },
                {
                    piece.Piece.create(
                        Position(row, right),
                        UP,
                        DOWN,
                    )
                    for row in range(top + 1, bottom)
                },
                {
                    piece.Piece.create(
                        Position(top, col),
                        LEFT,
                        RIGHT,
                    )
                    for col in range(left + 1, right)
                },
                {
                    piece.Piece.create(
                        Position(bottom, col),
                        LEFT,
                        RIGHT,
                    )
                    for col in range(left + 1, right)
                },
                {
                    piece.Piece.create(
                        Position(top, left),
                        DOWN,
                        RIGHT,
                    ),
                    piece.Piece.create(
                        Position(top, right),
                        LEFT,
                        DOWN,
                    ),
                    piece.Piece.create(
                        Position(bottom, right),
                        UP,
                        LEFT,
                    ),
                    piece.Piece.create(
                        Position(bottom, left),
                        UP,
                        RIGHT,
                    ),
                },
            )
        )

    def debug_print(self) -> str:
        rows = {piece.position.row for piece in self.pieces}
        cols = {piece.position.col for piece in self.pieces}
        top = min(rows)
        bottom = max(rows)
        left = min(cols)
        right = max(cols)
        s = ""

        def piece_is(
            piece_: piece.Piece,
            reverse_direction: Direction,
            forward_direction: Direction,
        ) -> bool:
            return {
                (connection.reverse_direction, connection.forward_direction)
                for connection in piece_.connections
            } == {
                (reverse_direction, forward_direction),
                (forward_direction, reverse_direction),
            }

        def piece_char(piece_: piece.Piece) -> str:
            if piece_is(piece_, UP, DOWN):
                return "|"
            elif piece_is(piece_, LEFT, RIGHT):
                return "-"
            elif piece_is(piece_, UP, LEFT):
                return "┘"
            elif piece_is(piece_, UP, RIGHT):
                return "└"
            elif piece_is(piece_, DOWN, LEFT):
                return "┐"
            elif piece_is(piece_, DOWN, RIGHT):
                return "┌"
            else:
                return "?"

        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if piece_ := self.get(Position(row, col)):
                    s += piece_char(piece_)
                else:
                    s += " "
            s += "\n"
        return s

    @property
    def bounds(self) -> tuple[Position, Position]:
        if len(self) == 0:
            return (Position(0, 0), Position(0, 0))
        rows = {piece.position.row for piece in self.pieces}
        cols = {piece.position.col for piece in self.pieces}
        return Position(min(rows), min(cols)), Position(max(rows), max(cols))


from tracky.track.pieces import piece
