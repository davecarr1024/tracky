import pytest

from tracky.track.grid import DOWN, UP, Grid, Position
from tracky.track.piece import Connection, Piece


def test_ctor_no_piece() -> None:
    c = Connection(UP, DOWN)
    assert c.reverse_direction == UP
    assert c.forward_direction == DOWN
    assert c.piece is None


def test_ctor_piece() -> None:
    p = Piece(Position(0, 0))
    c = Connection(UP, DOWN, p)
    assert c.reverse_direction == UP
    assert c.forward_direction == DOWN
    assert c.piece is p
    assert c in p.connections
    assert c is p.connections_by_direction[UP]


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
    assert c.reverse_direction not in p.connections_by_direction
    c.piece = p
    assert c.piece is p
    assert c in p.connections
    assert c is p.connections_by_direction[UP]
    c.piece = None
    assert c.piece is None
    assert c not in p.connections
    assert c.reverse_direction not in p.connections_by_direction


def test_reverse_position() -> None:
    c = Connection(UP, DOWN)
    p = Piece(Position(0, 0))
    assert c.reverse_position is None
    c.piece = p
    assert c.reverse_position == Position(-1, 0)


def test_reverse_piece() -> None:
    c = Connection(UP, DOWN)
    p1 = Piece(Position(0, 0), connections=[c])
    assert c.reverse_piece is None
    p2 = Piece(Position(-1, 0), connections=[Connection(UP, DOWN)])
    Grid(pieces=[p1, p2])
    assert c.reverse_piece is p2


def test_forward_position() -> None:
    c = Connection(UP, DOWN)
    p = Piece(Position(0, 0))
    assert c.forward_position is None
    c.piece = p
    assert c.forward_position == Position(1, 0)


def test_forward_piece() -> None:
    c = Connection(UP, DOWN)
    p1 = Piece(Position(0, 0), connections=[c])
    assert c.forward_piece is None
    p2 = Piece(Position(1, 0), connections=[Connection(UP, DOWN)])
    Grid(pieces=[p1, p2])
    assert c.forward_piece is p2


def test_invalid_piece() -> None:
    p = Piece(Position(0, 0))
    c = Connection(UP, DOWN, piece=p)
    with (
        pytest.raises(Connection.ValidationError),
        p._pause_validation(),  # type:ignore
        c._pause_validation(),  # type:ignore
    ):
        p._Piece__connections = frozenset[Connection]()  # type:ignore


def test_connected_connections() -> None:
    p1_going_down = Connection(UP, DOWN)
    p1_going_up = Connection(DOWN, UP)
    p1 = Piece(
        Position(0, 0),
        connections={
            p1_going_down,
            p1_going_up,
        },
    )
    p2_going_down = Connection(UP, DOWN)
    p2_going_up = Connection(DOWN, UP)
    p2 = Piece(
        Position(1, 0),
        connections={
            p2_going_down,
            p2_going_up,
        },
    )
    Grid(pieces=[p1, p2])

    assert p1_going_down.forward_direction is DOWN
    assert p1_going_down.forward_position == p2.position
    assert p1_going_down.forward_piece is p2
    assert p1_going_down.forward_connection is p2_going_down

    assert p1_going_down.reverse_direction is UP
    assert p1_going_down.reverse_position == Position(-1, 0)
    assert p1_going_down.reverse_piece is None
    assert p1_going_down.reverse_connection is None

    assert p1_going_up.forward_direction is UP
    assert p1_going_up.forward_position == Position(-1, 0)
    assert p1_going_up.forward_piece is None
    assert p1_going_up.forward_connection is None

    assert p1_going_up.reverse_direction is DOWN
    assert p1_going_up.reverse_position == p2.position
    assert p1_going_up.reverse_piece is p2
    assert p1_going_up.reverse_connection is p2_going_down

    assert p2_going_up.forward_direction is UP
    assert p2_going_up.forward_position == p1.position
    assert p2_going_up.forward_piece is p1
    assert p2_going_up.forward_connection is p1_going_up

    assert p2_going_up.reverse_direction is DOWN
    assert p2_going_up.reverse_position == Position(2, 0)
    assert p2_going_up.reverse_piece is None
    assert p2_going_up.reverse_connection is None

    assert p2_going_down.forward_direction is DOWN
    assert p2_going_down.forward_position == Position(2, 0)
    assert p2_going_down.forward_piece is None
    assert p2_going_down.forward_connection is None

    assert p2_going_down.reverse_direction is UP
    assert p2_going_down.reverse_position == p1.position
    assert p2_going_down.reverse_piece is p1
    assert p2_going_down.reverse_connection is p1_going_up
