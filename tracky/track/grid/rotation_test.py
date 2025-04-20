from pytest_subtests import SubTests

from tracky.track.grid import Direction, Rotation


def test_neg() -> None:
    assert -Rotation(2) == Rotation(2)


def test_add() -> None:
    assert Rotation(1) + Rotation(2) == Rotation(3)


def test_sub() -> None:
    assert Rotation(3) - Rotation(2) == Rotation(1)


def test_ctor_mod() -> None:
    assert Rotation(1) == Rotation(1)
    assert Rotation(5) == Rotation(1)
    assert Rotation(-3) == Rotation(1)


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
                Direction.LEFT,
                Direction.LEFT,
            ),
            (
                Rotation(0),
                Direction.UP,
                Direction.UP,
            ),
            (
                Rotation(0),
                Direction.RIGHT,
                Direction.RIGHT,
            ),
            (
                Rotation(0),
                Direction.DOWN,
                Direction.DOWN,
            ),
            (
                Rotation(1),
                Direction.LEFT,
                Direction.UP,
            ),
            (
                Rotation(1),
                Direction.UP,
                Direction.RIGHT,
            ),
            (
                Rotation(1),
                Direction.RIGHT,
                Direction.DOWN,
            ),
            (
                Rotation(2),
                Direction.DOWN,
                Direction.UP,
            ),
            (
                Rotation(2),
                Direction.LEFT,
                Direction.RIGHT,
            ),
            (
                Rotation(2),
                Direction.UP,
                Direction.DOWN,
            ),
            (
                Rotation(2),
                Direction.RIGHT,
                Direction.LEFT,
            ),
            (
                Rotation(2),
                Direction.DOWN,
                Direction.UP,
            ),
            (
                Rotation(3),
                Direction.LEFT,
                Direction.DOWN,
            ),
            (
                Rotation(3),
                Direction.UP,
                Direction.LEFT,
            ),
            (
                Rotation(3),
                Direction.RIGHT,
                Direction.UP,
            ),
            (
                Rotation(3),
                Direction.DOWN,
                Direction.RIGHT,
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
