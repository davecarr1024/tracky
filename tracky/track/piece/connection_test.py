import pytest

from tracky.track.grid import DOWN, UP, Grid, Position
from tracky.track.piece import Connection, Piece


def test_ctor_no_piece() -> None:
    c = Connection(UP, DOWN)
    assert c.from_direction == UP
    assert c.to_direction == DOWN
    assert c.piece is None


def test_ctor_piece() -> None:
    p = Piece(Position(0, 0))
    c = Connection(UP, DOWN, p)
    assert c.from_direction == UP
    assert c.to_direction == DOWN
    assert c.piece is p
    assert c in p.connections
    assert c is p.connections_by_from_direction[UP]


def test_eq() -> None:
    c = Connection(UP, DOWN)
    assert c == c
    assert c != Connection(UP, DOWN)
    assert hash(c) == hash(c)
    assert hash(c) != hash(Connection(UP, DOWN))


def test_set_piece() -> None:
    c = Connection(UP, DOWN)
    p = Piece(Position(0, 0))
    assert c.piece is None
    assert c not in p.connections
    assert c.from_direction not in p.connections_by_from_direction
    c.piece = p
    assert c.piece is p
    assert c in p.connections
    assert c is p.connections_by_from_direction[UP]
    c.piece = None
    assert c.piece is None
    assert c not in p.connections
    assert c.from_direction not in p.connections_by_from_direction


def test_from_position() -> None:
    c = Connection(UP, DOWN)
    p = Piece(Position(0, 0))
    assert c.from_position is None
    c.piece = p
    assert c.from_position == Position(-1, 0)


def test_from_piece() -> None:
    c = Connection(UP, DOWN)
    p1 = Piece(Position(0, 0), connections=[c])
    assert c.from_piece is None
    p2 = Piece(Position(-1, 0), connections=[Connection(UP, DOWN)])
    Grid(pieces=[p1, p2])
    assert c.from_piece is p2


def test_to_position() -> None:
    c = Connection(UP, DOWN)
    p = Piece(Position(0, 0))
    assert c.to_position is None
    c.piece = p
    assert c.to_position == Position(1, 0)


def test_to_piece() -> None:
    c = Connection(UP, DOWN)
    p1 = Piece(Position(0, 0), connections=[c])
    assert c.to_piece is None
    p2 = Piece(Position(1, 0), connections=[Connection(UP, DOWN)])
    Grid(pieces=[p1, p2])
    assert c.to_piece is p2


def test_invalid_piece() -> None:
    p = Piece(Position(0, 0))
    c = Connection(UP, DOWN, piece=p)
    with (
        pytest.raises(Connection.ValidationError),
        p._pause_validation(),  # type:ignore
        c._pause_validation(),  # type:ignore
    ):
        p._Piece__connections = frozenset[Connection]()  # type:ignore
