import pytest
from pytest_subtests import SubTests

from tracky.track.grid import DOWN, LEFT, RIGHT, UP, Direction, Position


def test_add(subtests: SubTests) -> None:
    for position, direction, expected in list[tuple[Position, Direction, Position]](
        [
            (Position(0, 0), RIGHT, Position(0, 1)),
            (Position(0, 0), LEFT, Position(0, -1)),
            (Position(0, 0), UP, Position(-1, 0)),
            (Position(0, 0), DOWN, Position(1, 0)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert position + direction == expected


def test_sub(subtests: SubTests) -> None:
    for position, direction, expected in list[tuple[Position, Direction, Position]](
        [
            (Position(0, 0), RIGHT, Position(0, -1)),
            (Position(0, 0), LEFT, Position(0, 1)),
            (Position(0, 0), UP, Position(1, 0)),
            (Position(0, 0), DOWN, Position(-1, 0)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert position - direction == expected


def test_invalid_values():
    with pytest.raises(Direction.ValueError):
        Direction(0, 0)
