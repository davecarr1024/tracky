from typing import Optional

import pytest
from pytest_subtests import SubTests

from tracky.track import Connection, Direction, GridPosition, Piece, TrackPosition
from tracky.visuals import Projection, Rectangle, Vector


def test_grid_width() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    assert projection.grid_num_rows == 6
    assert projection.grid_num_cols == 8
    assert projection.grid_max == GridPosition(11, 18)


def test_grid_to_screen(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, expected in list[tuple[GridPosition, Optional[Vector]]](
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
                Vector(0, 0),
            ),
            (
                GridPosition(6, 10),
                Vector(0, 100),
            ),
            (
                GridPosition(5, 11),
                Vector(100, 0),
            ),
            (
                GridPosition(10, 17),
                Vector(700, 500),
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
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, expected in list[tuple[Vector, Optional[GridPosition]]](
        [
            (Vector(-1, 0), None),
            (Vector(0, -1), None),
            (Vector(0, 801), None),
            (Vector(0, 601), None),
            (Vector(0, 0), GridPosition(5, 10)),
            (Vector(99, 99), GridPosition(5, 10)),
            (Vector(100, 100), GridPosition(6, 11)),
            (Vector(799, 599), GridPosition(10, 17)),
            (Vector(800, 600), None),
        ]
    ):
        with subtests.test(position=position, expected=expected):
            assert projection.screen_to_grid(position) == expected


def test_tile_center() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    assert projection.tile_center(GridPosition(6, 12)) == Vector(250, 150)


def test_tile_side(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, direction, expected in list[tuple[GridPosition, Direction, Optional[Vector]]](
        [
            (GridPosition(0, 0), Direction.LEFT, None),
            (GridPosition(5, 10), Direction.LEFT, Vector(0, 50)),
            (GridPosition(5, 10), Direction.UP, Vector(50, 0)),
            (GridPosition(5, 10), Direction.RIGHT, Vector(100, 50)),
            (GridPosition(5, 10), Direction.DOWN, Vector(50, 100)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert projection.tile_side(position, direction) == expected


def test_tile_corner(subtests: SubTests) -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    for position, directions, expected in list[
        tuple[
            GridPosition,
            tuple[Direction, Direction],
            Optional[Vector],
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
                Vector(0, 0),
            ),
            (
                GridPosition(5, 10),
                (Direction.RIGHT, Direction.UP),
                Vector(100, 0),
            ),
            (
                GridPosition(5, 10),
                (Direction.RIGHT, Direction.DOWN),
                Vector(100, 100),
            ),
            (
                GridPosition(5, 10),
                (Direction.LEFT, Direction.DOWN),
                Vector(0, 100),
            ),
        ]
    ):
        with subtests.test(position=position, directions=directions, expected=expected):
            assert projection.tile_corner(position, directions) == expected


def test_tile_corner_invalid_directions() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    with pytest.raises(Projection.ValueError):
        projection.tile_corner(GridPosition(5, 10), (Direction.LEFT, Direction.RIGHT))


def test_connection_ends() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(5, 10), connections={c})
    assert projection.connection_ends(c) == (Vector(0, 50), Vector(50, 0))


def test_connection_ends_disconnected() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    assert projection.connection_ends(c) is None


def test_connection_ends_off_grid() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(0, 0), connections={c})
    assert projection.connection_ends(c) is None


def test_connection_lerp() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(5, 10), connections={c})
    assert projection.connection_lerp(c, 0.5) == Vector(25, 25)


def test_track_to_screen() -> None:
    projection = Projection(
        Rectangle(Vector(0, 0), Vector(800, 600)),
        GridPosition(5, 10),
        tile_size=100,
    )
    c = Connection(Direction.LEFT, Direction.UP)
    Piece(GridPosition(5, 10), connections={c})
    assert projection.track_to_screen(TrackPosition(c, 0.5)) == Vector(25, 25)
