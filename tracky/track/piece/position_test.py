import pytest

from tracky.track.grid import LEFT, RIGHT, Grid
from tracky.track.grid import Position as GridPosition
from tracky.track.piece import Piece
from tracky.track.piece import Position as TrackPosition


def test_get_piece() -> None:
    piece = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    grid = Grid(pieces={piece})
    pos = TrackPosition(piece.connection(LEFT), 0)
    assert pos.piece is piece
    assert pos.grid is grid
    assert pos.grid_position == GridPosition(0, 0)


def test_add() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), RIGHT, 2)
    Grid(pieces={p1, p2})
    pos = TrackPosition(p1.connection(LEFT), 0)
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
