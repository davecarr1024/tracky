from pytest_subtests import SubTests

from tracky.track.grid import DOWN, LEFT, RIGHT, UP, Direction, Rotation


def test_mul(subtests: SubTests) -> None:
    for rotation, direction, expected in list[
        tuple[
            Rotation,
            Direction,
            Direction,
        ]
    ](
        [
            (
                Rotation(0),
                LEFT,
                LEFT,
            ),
            (
                Rotation(0),
                UP,
                UP,
            ),
            (
                Rotation(0),
                RIGHT,
                RIGHT,
            ),
            (
                Rotation(0),
                DOWN,
                DOWN,
            ),
            (
                Rotation(1),
                LEFT,
                UP,
            ),
            (
                Rotation(1),
                UP,
                RIGHT,
            ),
            (
                Rotation(1),
                RIGHT,
                DOWN,
            ),
            (
                Rotation(2),
                DOWN,
                UP,
            ),
            (
                Rotation(2),
                LEFT,
                RIGHT,
            ),
            (
                Rotation(2),
                UP,
                DOWN,
            ),
            (
                Rotation(2),
                RIGHT,
                LEFT,
            ),
            (
                Rotation(2),
                DOWN,
                UP,
            ),
            (
                Rotation(3),
                LEFT,
                DOWN,
            ),
            (
                Rotation(3),
                UP,
                LEFT,
            ),
            (
                Rotation(3),
                RIGHT,
                UP,
            ),
            (
                Rotation(3),
                DOWN,
                RIGHT,
            ),
        ]
    ):
        with subtests.test(
            rotation=rotation,
            direction=direction,
            expected=expected,
        ):
            assert rotation * direction == expected
            assert direction * rotation == expected
