from pytest_subtests import SubTests

from tracky.track.grid import Direction, Position


def test_add(subtests: SubTests) -> None:
    for position, direction, expected in list[tuple[Position, Direction, Position]](
        [
            (Position(0, 0), Direction.RIGHT, Position(0, 1)),
            (Position(0, 0), Direction.LEFT, Position(0, -1)),
            (Position(0, 0), Direction.UP, Position(-1, 0)),
            (Position(0, 0), Direction.DOWN, Position(1, 0)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert position + direction == expected


def test_sub(subtests: SubTests) -> None:
    for position, direction, expected in list[tuple[Position, Direction, Position]](
        [
            (Position(0, 0), Direction.RIGHT, Position(0, -1)),
            (Position(0, 0), Direction.LEFT, Position(0, 1)),
            (Position(0, 0), Direction.UP, Position(1, 0)),
            (Position(0, 0), Direction.DOWN, Position(-1, 0)),
        ]
    ):
        with subtests.test(position=position, direction=direction, expected=expected):
            assert position - direction == expected
