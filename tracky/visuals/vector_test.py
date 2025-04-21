from pytest_subtests import SubTests

from tracky.visuals.vector import Vector


def test_neg() -> None:
    assert -Vector(1, 2) == Vector(-1, -2)


def test_add() -> None:
    assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)


def test_sub() -> None:
    assert Vector(1, 2) - Vector(3, 4) == Vector(-2, -2)


def test_mul() -> None:
    assert Vector(1, 2) * 3 == Vector(3, 6)


def test_div() -> None:
    assert Vector(5, 10) // 5 == Vector(1, 2)


def test_lt() -> None:
    assert Vector(1, 2) < Vector(2, 3)
    assert not Vector(1, 2) < Vector(1, 3)  # x equal, y greater
    assert not Vector(1, 2) < Vector(2, 2)  # x greater, y equal
    assert not Vector(1, 2) < Vector(0, 1)  # both smaller
    assert not Vector(1, 2) < Vector(1, 2)  # equal


def test_le() -> None:
    assert Vector(1, 2) <= Vector(2, 3)
    assert Vector(1, 2) <= Vector(1, 2)
    assert not Vector(1, 2) <= Vector(0, 2)
    assert not Vector(1, 2) <= Vector(1, 1)
    assert not Vector(1, 2) <= Vector(0, 1)


def test_gt() -> None:
    assert Vector(2, 3) > Vector(1, 2)
    assert not Vector(2, 3) > Vector(2, 2)  # x equal, y smaller
    assert not Vector(2, 3) > Vector(3, 3)  # x greater, y equal
    assert not Vector(2, 3) > Vector(2, 4)  # y greater, x equal
    assert not Vector(2, 3) > Vector(2, 3)  # equal


def test_ge() -> None:
    assert Vector(2, 3) >= Vector(1, 2)
    assert Vector(2, 3) >= Vector(2, 3)
    assert not Vector(2, 3) >= Vector(3, 3)
    assert not Vector(2, 3) >= Vector(2, 4)
    assert not Vector(2, 3) >= Vector(3, 2)


def test_lerp(subtests: SubTests) -> None:
    for lhs, rhs, u, expected in list[tuple[Vector, Vector, float, Vector]](
        [
            (
                Vector(0, 0),
                Vector(100, 50),
                0,
                Vector(0, 0),
            ),
            (
                Vector(0, 0),
                Vector(100, 50),
                0.5,
                Vector(50, 25),
            ),
            (
                Vector(0, 0),
                Vector(100, 50),
                1,
                Vector(100, 50),
            ),
        ]
    ):
        with subtests.test(lhs=lhs, rhs=rhs, u=u, expected=expected):
            assert lhs.lerp(rhs, u) == expected
