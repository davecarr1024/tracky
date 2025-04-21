from typing import Optional, SupportsFloat

from pytest_subtests import SubTests

from tracky.track import Connection, ConnectionShape, Direction, GridPosition, Piece, TrackPosition
from tracky.visuals import Position, Projection, Rectangle, Rotation


def test_grid_width() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    assert projection.grid_num_rows == 6
    assert projection.grid_num_cols == 8
    assert projection.grid_max == GridPosition(11, 18)


def test_grid_to_screen(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, expected in list[tuple[GridPosition, Optional[Position]]](
        [
            (
                GridPosition(4, 10),
                None,
            ),
            (
                GridPosition(5, 9),
                None,
            ),
            (
                GridPosition(5, 19),
                None,
            ),
            (
                GridPosition(12, 18),
                None,
            ),
            (
                GridPosition(5, 10),
                Position(0, 0),
            ),
            (
                GridPosition(6, 10),
                Position(0, 100),
            ),
            (
                GridPosition(5, 11),
                Position(100, 0),
            ),
            (
                GridPosition(10, 17),
                Position(700, 500),
            ),
            (
                GridPosition(11, 18),
                None,
            ),
        ]
    ):
        with subtests.test(position=position, expected=expected):
            assert projection.grid_to_screen(position) == expected


def test_screen_to_grid(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, expected in list[tuple[Position, Optional[GridPosition]]](
        [
            (Position(-1, 0), None),
            (Position(0, -1), None),
            (Position(0, 801), None),
            (Position(0, 601), None),
            (Position(0, 0), GridPosition(5, 10)),
            (Position(99, 99), GridPosition(5, 10)),
            (Position(100, 100), GridPosition(6, 11)),
            (Position(799, 599), GridPosition(10, 17)),
            (Position(800, 600), None),
        ]
    ):
        with subtests.test(position=position, expected=expected):
            assert projection.screen_to_grid(position) == expected


def test_tile_center() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    assert projection.tile_center(GridPosition(6, 12)) == Position(250, 150)


def test_tile_side(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, direction, expected in list[tuple[GridPosition, Direction, Optional[Position]]](
        [
            (GridPosition(0, 0), Direction.LEFT, None),
            (GridPosition(5, 10), Direction.LEFT, Position(0, 50)),
            (GridPosition(5, 10), Direction.UP, Position(50, 0)),
            (GridPosition(5, 10), Direction.RIGHT, Position(100, 50)),
            (GridPosition(5, 10), Direction.DOWN, Position(50, 100)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert projection.tile_side(position, direction) == expected


def test_tile_corner(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, directions, expected in list[
        tuple[
            GridPosition,
            tuple[Direction, Direction],
            Optional[Position],
        ]
    ](
        [
            (
                GridPosition(0, 0),
                (Direction.LEFT, Direction.UP),
                None,
            ),
            (
                GridPosition(5, 10),
                (Direction.LEFT, Direction.UP),
                Position(0, 0),
            ),
            (
                GridPosition(5, 10),
                (Direction.RIGHT, Direction.UP),
                Position(100, 0),
            ),
            (
                GridPosition(5, 10),
                (Direction.RIGHT, Direction.DOWN),
                Position(100, 100),
            ),
            (
                GridPosition(5, 10),
                (Direction.LEFT, Direction.DOWN),
                Position(0, 100),
            ),
            (
                GridPosition(5, 10),
                (Direction.LEFT, Direction.RIGHT),
                None,
            ),
        ]
    ):
        with subtests.test(position=position, directions=directions, expected=expected):
            assert projection.tile_corner(position, directions) == expected


def test_connection_ends() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(5, 10), connections={c})
    assert projection.connection_ends(c) == (Position(0, 50), Position(50, 0))


def test_connection_ends_disconnected() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    assert projection.connection_ends(c) is None


def test_connection_ends_off_grid() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(0, 0), connections={c})
    assert projection.connection_ends(c) is None


def test_connection_lerp(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for name, c, u, expected in list[
        tuple[
            str,
            Connection,
            SupportsFloat,
            Optional[tuple[Position, Rotation]],
        ]
    ](
        [
            (
                "disconnected",
                Connection(Direction.LEFT, Direction.UP),
                0,
                None,
            ),
            (
                "off grid",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(0, 0),
                    ),
                ),
                0,
                None,
            ),
            (
                "left-up straight 0",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.STRAIGHT,
                    ),
                ),
                0,
                (
                    Position(0, 50),
                    Rotation.from_degrees(-45),
                ),
            ),
            (
                "left-up straight 0.5",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.STRAIGHT,
                    ),
                ),
                0.5,
                (
                    Position(25, 25),
                    Rotation.from_degrees(-45),
                ),
            ),
            (
                "left-up straight 1",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.STRAIGHT,
                    ),
                ),
                1,
                (
                    Position(50, 0),
                    Rotation.from_degrees(-45),
                ),
            ),
            (
                "left-up curved 0",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                0,
                (
                    Position(0, 50),
                    Rotation.from_degrees(0),
                ),
            ),
            (
                "left-up curved 0.5",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                0.5,
                (
                    Position(35, 35),
                    Rotation.from_degrees(-45),
                ),
            ),
            (
                "left-up curved 1",
                Connection(
                    Direction.LEFT,
                    Direction.UP,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                1,
                (
                    Position(50, 0),
                    Rotation.from_degrees(-90),
                ),
            ),
            (
                "left-right curved 0",
                Connection(
                    Direction.LEFT,
                    Direction.RIGHT,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                0,
                (
                    Position(0, 50),
                    Rotation.from_degrees(0),
                ),
            ),
            (
                "left-right curved 0.5",
                Connection(
                    Direction.LEFT,
                    Direction.RIGHT,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                0.5,
                (
                    Position(50, 50),
                    Rotation.from_degrees(0),
                ),
            ),
            (
                "left-right curved 1",
                Connection(
                    Direction.LEFT,
                    Direction.RIGHT,
                    piece=Piece(
                        GridPosition(5, 10),
                        connection_shape=ConnectionShape.CURVED,
                    ),
                ),
                1,
                (
                    Position(100, 50),
                    Rotation.from_degrees(0),
                ),
            ),
        ]
    ):
        with subtests.test(name=name, c=c, u=u, expected=expected):
            assert projection.connection_lerp(c, u) == expected


def test_track_to_screen() -> None:
    projection = Projection(
        Rectangle(Position(0, 0), Position(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(5, 10), connections={c})
    assert projection.track_to_screen(TrackPosition(c, 0.5)) == (
        Position(25, 25),
        Rotation.from_degrees(-45),
    )
