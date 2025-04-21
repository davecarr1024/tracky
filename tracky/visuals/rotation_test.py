from math import pi
from typing import SupportsFloat

from pytest_subtests import SubTests

from tracky.track import Direction
from tracky.visuals import Offset, Rotation


def test_from_radians(subtests: SubTests) -> None:
    for radians, expected in list[tuple[SupportsFloat, SupportsFloat]](
        [
            (0, 0),
            (pi / 2, pi / 2),
            (pi, -pi),
            (3 * pi / 2, -pi / 2),
            (2 * pi, 0),
            (-pi / 2, -pi / 2),
            (-pi, -pi),
            (-3 * pi / 2, pi / 2),
            (-2 * pi, 0),
        ]
    ):
        with subtests.test(radians=radians, expected=expected):
            assert Rotation.from_radians(radians).radians == expected


def test_from_degrees(subtests: SubTests) -> None:
    for degrees, expected in list[tuple[SupportsFloat, SupportsFloat]](
        [
            (0, 0),
            (90, 90),
            (180, -180),
            (270, -90),
            (360, 0),
            (-90, -90),
            (-180, -180),
            (-270, 90),
            (-360, 0),
        ]
    ):
        with subtests.test(degrees=degrees, expected=expected):
            assert Rotation.from_degrees(degrees).degrees == expected


def test_neg() -> None:
    assert -Rotation.from_degrees(90) == Rotation.from_degrees(-90)


def test_add() -> None:
    assert Rotation.from_degrees(30) + Rotation.from_degrees(90) == Rotation.from_degrees(120)


def test_sub() -> None:
    assert Rotation.from_degrees(120) - Rotation.from_degrees(90) == Rotation.from_degrees(30)


def test_mul_float() -> None:
    assert Rotation.from_degrees(30) * 2 == Rotation.from_degrees(60)


def test_mul_offset() -> None:
    assert Rotation.from_degrees(-90) * Offset(0, 1) == Offset(1, 0)


def test_lerp(subtests: SubTests) -> None:
    for lhs, rhs, u, expected in list[
        tuple[
            Rotation,
            Rotation,
            SupportsFloat,
            Rotation,
        ]
    ](
        [
            (
                Rotation.from_degrees(0),
                Rotation.from_degrees(90),
                0,
                Rotation.from_degrees(0),
            ),
            (
                Rotation.from_degrees(0),
                Rotation.from_degrees(90),
                0.5,
                Rotation.from_degrees(45),
            ),
            (Rotation.from_degrees(0), Rotation.from_degrees(90), 1, Rotation.from_degrees(90)),
            (
                Rotation.from_degrees(0),
                Rotation.from_degrees(-90),
                0,
                Rotation.from_degrees(0),
            ),
            (
                Rotation.from_degrees(0),
                Rotation.from_degrees(-90),
                0.5,
                Rotation.from_degrees(-45),
            ),
            (
                Rotation.from_degrees(0),
                Rotation.from_degrees(-90),
                1,
                Rotation.from_degrees(-90),
            ),
            (
                Rotation.from_degrees(175),
                Rotation.from_degrees(-175),
                0,
                Rotation.from_degrees(175),
            ),
            (
                Rotation.from_degrees(175),
                Rotation.from_degrees(-175),
                0.5,
                Rotation.from_degrees(-180),
            ),
            (
                Rotation.from_degrees(175),
                Rotation.from_degrees(-175),
                1,
                Rotation.from_degrees(-175),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, u=u, expected=expected):
            assert lhs.lerp(rhs, u) == expected


def test_from_direction(subtests: SubTests) -> None:
    for direction, expected in list[tuple[Direction, Rotation]](
        [
            (
                Direction.LEFT,
                Rotation.from_degrees(180),
            ),
            (
                Direction.UP,
                Rotation.from_degrees(-90),
            ),
            (
                Direction.RIGHT,
                Rotation.from_degrees(0),
            ),
            (
                Direction.DOWN,
                Rotation.from_degrees(90),
            ),
        ]
    ):
        with subtests.test(direction=direction, expected=expected):
            assert Rotation.from_direction(direction) == expected
