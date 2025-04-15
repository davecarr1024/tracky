import pytest

from tracky.track.grid import Grid, Position
from tracky.track.piece import Piece


def test_ctor_empty() -> None:
    grid = Grid()
    assert dict(grid) == {}
    assert grid.pieces == set()


def test_ctor_pieces() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid(pieces=[piece])
    assert dict(grid) == {Position(0, 0): piece}
    assert grid.pieces == {piece}
    assert piece.grid is grid
    assert grid[piece.position] is piece


def test_eq() -> None:
    grid = Grid()
    assert grid == grid
    assert grid != Grid()
    assert hash(grid) == hash(grid)
    assert hash(grid) != hash(Grid())


def test_set_pieces() -> None:
    grid = Grid()
    piece = Piece(Position(0, 0))
    grid.pieces |= {piece}
    assert dict(grid) == {Position(0, 0): piece}
    assert grid.pieces == {piece}
    assert piece.grid is grid
    grid.pieces -= {piece}
    assert dict(grid) == {}
    assert grid.pieces == set()
    assert piece.grid is None


def test_add_piece() -> None:
    grid = Grid()
    piece = Piece(Position(0, 0))
    assert piece.grid is None
    assert dict(grid) == {}
    assert grid.pieces == set()
    grid.add_piece(piece)
    assert dict(grid) == {Position(0, 0): piece}
    assert grid.pieces == {piece}
    assert piece.grid is grid


def test_remove_piece() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid(pieces={piece})
    assert dict(grid) == {Position(0, 0): piece}
    assert grid.pieces == {piece}
    assert piece.grid is grid
    grid.remove_piece(piece)
    assert dict(grid) == {}
    assert grid.pieces == set()
    assert piece.grid is None


def test_pieces_by_position() -> None:
    piece1 = Piece(Position(0, 0))
    piece2 = Piece(Position(1, 0))
    grid = Grid(pieces={piece1, piece2})
    assert grid.pieces_by_position == {
        piece1.position: piece1,
        piece2.position: piece2,
    }


def test_getitem() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid(pieces={piece})
    assert grid[piece.position] is piece
    assert grid.get(Position(1, 2)) is None


def test_setitem() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid()
    grid[piece.position] = piece
    assert grid[piece.position] is piece
    assert grid.pieces == {piece}
    assert piece.grid is grid


def test_setitem_invalid_position() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid()
    with pytest.raises(Grid.ValidationError):
        grid[Position(1, 2)] = piece


def test_delitem() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid(pieces={piece})
    del grid[piece.position]
    assert piece.position not in grid
    assert grid.pieces == set()


def test_delitem_keyerror() -> None:
    grid = Grid()
    with pytest.raises(Grid.KeyError):
        del grid[Position(0, 0)]


def test_invalid_piece() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid(pieces={piece})
    with (
        pytest.raises(Grid.ValidationError),
        piece._pause_validation(),  # type: ignore
        grid._pause_validation(),  # type: ignore
    ):
        piece._Piece__grid = None  # type: ignore


def test_duplicate_piece_positions() -> None:
    piece1 = Piece(Position(0, 0))
    piece2 = Piece(Position(0, 0))
    with pytest.raises(Grid.ValidationError):
        Grid(pieces={piece1, piece2})
