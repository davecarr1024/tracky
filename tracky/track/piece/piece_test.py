import pytest

from tracky.track.grid import DOWN, RIGHT, UP, Grid, Position
from tracky.track.piece import Connection, Piece


def test_ctor_empty() -> None:
    piece = Piece(Position(0, 0))
    assert piece.position == Position(0, 0)
    assert piece.grid is None
    assert piece.connections == frozenset()


def test_ctor_grid() -> None:
    grid = Grid()
    piece = Piece(Position(0, 0), grid=grid)
    assert piece.position == Position(0, 0)
    assert piece.grid == grid
    assert piece.connections == frozenset()


def test_ctor_connections() -> None:
    connection = Connection(UP, DOWN)
    piece = Piece(Position(0, 0), connections={connection})
    assert piece.connections == {connection}
    assert piece.grid is None
    assert piece.position == Position(0, 0)


def test_eq() -> None:
    piece = Piece(Position(0, 0))
    assert piece == piece
    assert piece != Piece(Position(0, 0))
    assert hash(piece) == hash(piece)
    assert hash(piece) != hash(Piece(Position(0, 0)))


def test_set_grid() -> None:
    piece = Piece(Position(0, 0))
    grid = Grid()
    assert piece.grid is None
    assert piece not in grid.pieces
    assert piece.position not in grid
    piece.grid = grid
    assert piece.grid == grid
    assert grid.pieces == {piece}
    assert grid[piece.position] == piece
    piece.grid = None
    assert piece.grid is None
    assert piece not in grid.pieces
    assert piece.position not in grid


def test_invalid_grid() -> None:
    grid = Grid()
    piece = Piece(Position(0, 0), grid=grid)
    with (
        pytest.raises(Piece.ValidationError),
        piece._pause_validation(),  # type: ignore
        grid._pause_validation(),  # type: ignore
    ):
        grid._Grid__pieces = frozenset()  # type: ignore


def test_duplicate_from_directions() -> None:
    connection1 = Connection(UP, DOWN)
    connection2 = Connection(UP, RIGHT)
    with pytest.raises(Piece.ValidationError):
        Piece(Position(0, 0), connections={connection1, connection2})


def test_connection() -> None:
    c = Connection(UP, DOWN)
    piece = Piece(Position(0, 0), connections={c})
    assert piece.connection(UP) is c
    assert piece.connection(DOWN) is None


def test_reverse_position() -> None:
    piece = Piece(Position(0, 0), connections={Connection(UP, DOWN)})
    assert piece.reverse_position(UP) == Position(-1, 0)


def test_reverse_piece() -> None:
    piece = Piece(Position(0, 0), connections={Connection(UP, DOWN)})
    grid = Grid(pieces={piece})
    assert piece.reverse_piece(UP) is None
    piece2 = Piece(Position(-1, 0))
    grid.add_piece(piece2)
    assert piece.reverse_piece(UP) is piece2


def test_forward_position() -> None:
    piece = Piece(Position(0, 0), connections={Connection(UP, DOWN)})
    assert piece.forward_position(UP) == Position(1, 0)


def test_forward_piece() -> None:
    piece = Piece(Position(0, 0), connections={Connection(UP, DOWN)})
    grid = Grid(pieces={piece})
    assert piece.forward_piece(UP) is None
    piece2 = Piece(Position(1, 0))
    grid.add_piece(piece2)
    assert piece.forward_piece(UP) is piece2
