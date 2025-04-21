from typing import SupportsFloat

from pytest_subtests import SubTests

from tracky.visuals import Offset, Position, Rotation


def test_add() -> None:
    assert Position(1, 2) + Offset(3, 4) == Position(4, 6)


def test_sub_position() -> None:
    assert Position(1, 2) - Position(3, 4) == Offset(-2, -2)


def test_sub_offset() -> None:
    assert Position(1, 2) - Offset(3, 4) == Position(-2, -2)


def test_lerp(subtests: SubTests) -> None:
    for lhs, rhs, u, expected in list[tuple[Position, Position, SupportsFloat, Position]](
        [
            (
                Position(0, 0),
                Position(10, 20),
                0,
                Position(0, 0),
            ),
            (
                Position(0, 0),
                Position(10, 20),
                0.5,
                Position(5, 10),
            ),
            (Position(0, 0), Position(10, 20), 1, Position(10, 20)),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, u=u, expected=expected):
            assert lhs.lerp(rhs, u) == expected


def test_direction_to() -> None:
    assert Position(1, 0).direction_to(Position(0, 1)) == Rotation.from_degrees(135)
