from typing import Iterable, Optional

import pytest
from pytest_subtests import SubTests

from tracky.track.grid import Direction, Grid, Position
from tracky.track.grid.rotation import Rotation
from tracky.track.pieces import Connection, ConnectionShape, Piece


def test_ctor_empty() -> None:
    piece = Piece(Position(0, 0))
    assert piece.position == Position(0, 0)
    assert piece.grid is None
    assert piece.connections == frozenset()
    assert piece.connection_shape is ConnectionShape.STRAIGHT


def test_ctor_connection_shape() -> None:
    piece = Piece(Position(0, 0), connection_shape=ConnectionShape.CURVED)
    assert piece.position == Position(0, 0)
    assert piece.connection_shape is ConnectionShape.CURVED


def test_ctor_grid() -> None:
    grid = Grid()
    piece = Piece(Position(0, 0), grid=grid)
    assert piece.position == Position(0, 0)
    assert piece.grid == grid
    assert piece.connections == frozenset()


def test_ctor_connections() -> None:
    connection = Connection(Direction.UP, Direction.DOWN)
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
    connection1 = Connection(Direction.UP, Direction.DOWN)
    connection2 = Connection(Direction.UP, Direction.RIGHT)
    with pytest.raises(Piece.ValidationError):
        Piece(Position(0, 0), connections={connection1, connection2})


def test_connection() -> None:
    c = Connection(Direction.UP, Direction.DOWN)
    piece = Piece(Position(0, 0), connections={c})
    assert piece.connection(Direction.UP) is c
    with pytest.raises(Piece.KeyError):
        piece.connection(Direction.DOWN)


def test_reverse_position() -> None:
    piece = Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)})
    assert piece.reverse_position(Direction.UP) == Position(-1, 0)


def test_reverse_piece() -> None:
    piece = Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)})
    grid = Grid(pieces={piece})
    assert piece.reverse_piece(Direction.UP) is None
    piece2 = Piece(Position(-1, 0))
    grid.add_piece(piece2)
    assert piece.reverse_piece(Direction.UP) is piece2


def test_forward_position() -> None:
    piece = Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)})
    assert piece.forward_position(Direction.UP) == Position(1, 0)


def test_forward_piece() -> None:
    piece = Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)})
    grid = Grid(pieces={piece})
    assert piece.forward_piece(Direction.UP) is None
    piece2 = Piece(Position(1, 0))
    grid.add_piece(piece2)
    assert piece.forward_piece(Direction.UP) is piece2


def assert_piece_is(
    piece: Piece,
    position: Position,
    connections: Iterable[tuple[Direction, Direction]],
) -> None:
    assert piece.position == position
    assert {(c.reverse_direction, c.forward_direction) for c in piece.connections} == set(
        connections
    )


def test_create() -> None:
    p = Piece.create(Position(0, 0), Direction.UP, Direction.DOWN)
    assert_piece_is(
        p, Position(0, 0), {(Direction.UP, Direction.DOWN), (Direction.DOWN, Direction.UP)}
    )


def test_create_line() -> None:
    line = list(Piece.create_line(Position(0, 0), Direction.RIGHT, 3))
    for i in range(3):
        assert_piece_is(
            line[i],
            Position(0, i),
            {(Direction.LEFT, Direction.RIGHT), (Direction.RIGHT, Direction.LEFT)},
        )


def test_rotate(subtests: SubTests) -> None:
    for piece, rotation, expected in list[tuple[Piece, Rotation, Piece]](
        [
            (
                Piece(Position(0, 0)),
                Rotation(0),
                Piece(Position(0, 0)),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Rotation(0),
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Rotation(2),
                Piece(Position(0, 0), connections={Connection(Direction.RIGHT, Direction.LEFT)}),
            ),
            (
                Piece(
                    Position(0, 0),
                    connections={
                        Connection(Direction.LEFT, Direction.RIGHT),
                        Connection(Direction.UP, Direction.DOWN),
                    },
                ),
                Rotation(1),
                Piece(
                    Position(0, 0),
                    connections={
                        Connection(Direction.UP, Direction.DOWN),
                        Connection(Direction.RIGHT, Direction.LEFT),
                    },
                ),
            ),
        ]
    ):
        with subtests.test(piece=piece, rotation=rotation, expected=expected):
            assert piece.rotate(rotation).is_same_as(expected)


def test_is_same_as(subtests: SubTests) -> None:
    for lhs, rhs, expected in list[tuple[Piece, Piece, bool]](
        [
            (
                Piece(Position(0, 0)),
                Piece(Position(0, 0)),
                True,
            ),
            (
                Piece(Position(0, 0)),
                Piece(Position(0, 1)),
                True,
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0)),
                False,
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)}),
                False,
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                True,
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs.is_same_as(rhs) == expected


def test_rotation_to(subtests: SubTests) -> None:
    for lhs, rhs, expected in list[tuple[Piece, Piece, Optional[Rotation]]](
        [
            (
                Piece(Position(0, 0)),
                Piece(Position(0, 0)),
                Rotation(0),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.UP)}),
                None,
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Rotation(0),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.UP, Direction.DOWN)}),
                Rotation(1),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.RIGHT, Direction.LEFT)}),
                Rotation(2),
            ),
            (
                Piece(Position(0, 0), connections={Connection(Direction.LEFT, Direction.RIGHT)}),
                Piece(Position(0, 0), connections={Connection(Direction.DOWN, Direction.UP)}),
                Rotation(3),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, expected=expected):
            assert lhs.rotation_to(rhs) == expected
            if expected is not None:
                assert lhs.rotate(expected).is_same_as(rhs)
