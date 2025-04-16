from collections import defaultdict
from typing import Iterable, Iterator, Mapping, MutableMapping, Optional, override

from tracky.core import Error, Validatable
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
                raise self._validation_error(
                    f"multiple pieces at position {position}: {pieces}"
                )

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


from tracky.track.pieces import piece
