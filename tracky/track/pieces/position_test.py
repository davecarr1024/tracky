import pytest

from tracky.track.grid import Direction, Grid
from tracky.track.grid import Position as GridPosition
from tracky.track.pieces import Piece
from tracky.track.pieces import Position as TrackPosition


def test_get_piece() -> None:
    piece = Piece.create(GridPosition(0, 0), Direction.LEFT, Direction.RIGHT)
    grid = Grid(pieces={piece})
    pos = TrackPosition(piece.connection(Direction.LEFT), 0)
    assert pos.piece is piece
    assert pos.grid is grid
    assert pos.grid_position == GridPosition(0, 0)


def test_add() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 2)
    Grid(pieces={p1, p2})
    pos = TrackPosition(p1.connection(Direction.LEFT), 0)
    with pytest.raises(TrackPosition.ValueError):
        _ = pos - 0.5
    pos += 0.5
    assert pos.piece is p1
    assert pos.u == 0.5
    pos += 1
    assert pos.piece is p2
    assert pos.u == 0.5
    with pytest.raises(TrackPosition.ValueError):
        _ = pos + 1
    pos -= 1
    assert pos.piece is p1
    assert pos.u == 0.5


def test_move_multiple_pieces() -> None:
    p1, p2, p3 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 3)
    Grid(pieces={p1, p2, p3})
    pos = TrackPosition(p1.connection(Direction.LEFT), 0.5)
    assert pos.piece is p1
    pos += 2
    assert pos.piece is p3
    pos -= 2
    assert pos.piece is p1


def test_with_u_same_piece() -> None:
    p1 = Piece.create(GridPosition(0, 0), Direction.LEFT, Direction.RIGHT)
    Grid(pieces={p1})
    pos = TrackPosition(p1.connection(Direction.LEFT), 0.5)
    assert pos.piece is p1
    assert pos.with_u(0.1).piece is p1


def test_with_u_one_piece_forward() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 2)
    Grid(pieces={p1, p2})
    pos = TrackPosition(p1.connection(Direction.LEFT), 0.5)
    assert pos.piece is p1
    assert pos.with_u(1.5).piece is p2


def test_with_u_two_pieces_forward() -> None:
    p1, p2, p3 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 3)
    Grid(pieces={p1, p2, p3})
    pos = TrackPosition(p1.connection(Direction.LEFT), 0.5)
    assert pos.piece is p1
    assert pos.with_u(2.5).piece is p3


def test_with_u_one_piece_reverse() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 2)
    Grid(pieces={p1, p2})
    pos = TrackPosition(p2.connection(Direction.LEFT), 0.5)
    assert pos.piece is p2
    assert pos.with_u(-0.5).piece is p1


def test_with_u_two_pieces_reverse() -> None:
    p1, p2, p3 = Piece.create_line(GridPosition(0, 0), Direction.RIGHT, 3)
    Grid(pieces={p1, p2, p3})
    pos = TrackPosition(p3.connection(Direction.LEFT), 0.5)
    assert pos.piece is p3
    assert pos.with_u(-2).piece is p1
