from typing import SupportsFloat

from pytest_subtests import SubTests

from tracky.visuals import Offset, Position, Rotation


def test_add_offset() -> None:
    assert Offset(1, 2) + Offset(3, 4) == Offset(4, 6)


def test_add_position() -> None:
    assert Offset(1, 2) + Position(3, 4) == Position(4, 6)


def test_neg() -> None:
    assert -Offset(1, 2) == Offset(-1, -2)


def test_sub() -> None:
    assert Offset(1, 2) - Offset(3, 4) == Offset(-2, -2)


def test_mul() -> None:
    assert Offset(1, 2) * 2 == Offset(2, 4)


def test_div() -> None:
    assert Offset(2, 4) // 2 == Offset(1, 2)


def test_length() -> None:
    assert Offset(3, 4).length == 5


def test_norm() -> None:
    assert Offset(100, 0).norm() == Offset(1, 0)


def test_as_rotation() -> None:
    assert Offset(0, 1).as_rotation() == Rotation.from_degrees(90)


def test_lerp(subtests: SubTests) -> None:
    for lhs, rhs, u, expected in list[tuple[Offset, Offset, SupportsFloat, Offset]](
        [
            (
                Offset(0, 0),
                Offset(10, 20),
                0,
                Offset(0, 0),
            ),
            (
                Offset(0, 0),
                Offset(10, 20),
                0.5,
                Offset(5, 10),
            ),
            (
                Offset(0, 0),
                Offset(10, 20),
                1,
                Offset(10, 20),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, u=u, expected=expected):
            assert lhs.lerp(rhs, u) == expected
