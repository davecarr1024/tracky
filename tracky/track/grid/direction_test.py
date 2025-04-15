from pytest_subtests import SubTests

from tracky.track.grid import DOWN, LEFT, RIGHT, UP, Direction


def test_neg(subtests: SubTests) -> None:
    for direction, expected in list[tuple[Direction, Direction]](
        [
            (UP, DOWN),
            (DOWN, UP),
            (LEFT, RIGHT),
            (RIGHT, LEFT),
        ]
    ):
        with subtests.test(direction=direction, expected=expected):
            assert -direction == expected
