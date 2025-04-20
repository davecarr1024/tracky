from pytest_subtests import SubTests

from tracky.track.grid import Direction


def test_neg(subtests: SubTests) -> None:
    for direction, expected in list[tuple[Direction, Direction]](
        [
            (Direction.UP, Direction.DOWN),
            (Direction.DOWN, Direction.UP),
            (Direction.LEFT, Direction.RIGHT),
            (Direction.RIGHT, Direction.LEFT),
        ]
    ):
        with subtests.test(direction=direction, expected=expected):
            assert -direction == expected
