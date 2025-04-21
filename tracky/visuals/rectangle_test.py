import pytest
from pytest_subtests import SubTests

from tracky.visuals import Offset, Position, Rectangle


def test_invalid_bounds() -> None:
    with pytest.raises(Rectangle.ValueError):
        Rectangle(Position(1, 1), Position(0, 0))


def test_size() -> None:
    assert Rectangle(Position(1, 2), Position(4, 3)).size == Offset(3, 1)


def test_width() -> None:
    assert Rectangle(Position(1, 2), Position(4, 3)).width == 3


def test_height() -> None:
    assert Rectangle(Position(1, 2), Position(4, 3)).height == 1


def test_contains(subtests: SubTests) -> None:
    for v, r, expected in list[tuple[Position, Rectangle, bool]](
        [
            (
                Position(0, 0),
                Rectangle(Position(0, 0), Position(10, 5)),
                True,
            ),
            (
                Position(9, 0),
                Rectangle(Position(0, 0), Position(10, 5)),
                True,
            ),
            (
                Position(0, 4),
                Rectangle(Position(0, 0), Position(10, 5)),
                True,
            ),
            (
                Position(9, 4),
                Rectangle(Position(0, 0), Position(10, 5)),
                True,
            ),
            (
                Position(-1, 0),
                Rectangle(Position(0, 0), Position(10, 5)),
                False,
            ),
            (
                Position(0, -1),
                Rectangle(Position(0, 0), Position(10, 5)),
                False,
            ),
            (
                Position(10, 4),
                Rectangle(Position(0, 0), Position(10, 5)),
                False,
            ),
            (
                Position(9, 5),
                Rectangle(Position(0, 0), Position(10, 5)),
                False,
            ),
        ]
    ):
        with subtests.test(v=v, r=r, expected=expected):
            assert (v in r) == expected
