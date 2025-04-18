import pytest

from tracky.track.grid import DOWN, LEFT, RIGHT, UP, Grid, Position
from tracky.track.pieces import Connection, Piece


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


def test_forward_connection() -> None:
    p1, p2 = Piece.create_line(Position(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    assert p1.connection(LEFT).forward_connection is p2.connection(LEFT)


def test_forward_connection_not_found() -> None:
    p1, p2 = Piece.create_line(Position(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    assert p2.connection(LEFT).forward_connection is None


def test_reverse_connection() -> None:
    p1, p2 = Piece.create_line(Position(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    assert p2.connection(LEFT).reverse_connection is p1.connection(LEFT)


def test_reverse_connection_not_found() -> None:
    p1, p2 = Piece.create_line(Position(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    assert p1.connection(LEFT).reverse_connection is None


def test_reverse_connection_trailing_switch() -> None:
    # a switch that joins LEFT and UP to RIGHT, but only goes RIGHT to UP
    p1_left_to_right = Connection(LEFT, RIGHT)
    p1_up_to_right = Connection(UP, RIGHT)
    p1_right_to_up = Connection(RIGHT, UP)
    p1 = Piece(Position(0, 0), connections=[p1_left_to_right, p1_up_to_right, p1_right_to_up])
    p2 = Piece.create(Position(0, 1), LEFT, RIGHT)
    Grid(pieces=[p1, p2])
    # If we go backwards from p2 LEFT-RIGHT, we should end up on p1 UP-RIGHT,
    # since that's how the switch is pointed.
    assert p2.connection(LEFT).reverse_connection is p1_up_to_right


def test_reverse_connection_unidirectional() -> None:
    # A derailer - goes one way but not the other.
    p1_left_to_right = Connection(LEFT, RIGHT)
    p1 = Piece(Position(0, 0), connections=[p1_left_to_right])
    p2 = Piece.create(Position(0, 1), LEFT, RIGHT)
    Grid(pieces=[p1, p2])
    # If we go backwards from p2 LEFT-RIGHT, we can't get back that way since there's no
    # entrance to p1 from the RIGHT, even though we're facing RIGHT.
    assert p2.connection(LEFT).reverse_connection is None
