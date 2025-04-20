import pytest
from pytest_subtests import SubTests

from tracky.visuals import Rectangle, Vector


def test_invalid_bounds() -> None:
    with pytest.raises(Rectangle.ValueError):
        Rectangle(Vector(1, 1), Vector(0, 0))


def test_size() -> None:
    assert Rectangle(Vector(1, 2), Vector(4, 3)).size == Vector(3, 1)


def test_width() -> None:
    assert Rectangle(Vector(1, 2), Vector(4, 3)).width == 3


def test_height() -> None:
    assert Rectangle(Vector(1, 2), Vector(4, 3)).height == 1


def test_contains(subtests: SubTests) -> None:
    for v, r, expected in list[tuple[Vector, Rectangle, bool]](
        [
            (
                Vector(0, 0),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                True,
            ),
            (
                Vector(10, 0),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                True,
            ),
            (
                Vector(0, 5),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                True,
            ),
            (
                Vector(10, 5),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                True,
            ),
            (
                Vector(-1, 0),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                False,
            ),
            (
                Vector(0, -1),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                False,
            ),
            (
                Vector(11, 5),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                False,
            ),
            (
                Vector(10, 6),
                Rectangle(Vector(0, 0), Vector(10, 5)),
                False,
            ),
        ]
    ):
        with subtests.test(v=v, r=r, expected=expected):
            assert (v in r) == expected
