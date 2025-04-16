import pytest
from pytest import approx  # type:ignore

from tracky.cars import Car, CarManager
from tracky.track import LEFT, RIGHT, Connection, Grid, GridPosition, Piece, TrackPosition


def test_ctor() -> None:
    c = Connection(LEFT, RIGHT)
    p = Piece(GridPosition(0, 0), connections={c})
    grid = Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0.5)
    car = Car(pos, length=2, mass=3, velocity_damping=-1)
    assert car.position == pos
    assert car.connection is p.connection(LEFT)
    assert car.piece is p
    assert car.grid is grid
    assert car.grid_position == GridPosition(0, 0)
    assert car.u == 0.5
    assert car.length == 2
    assert car.mass == 3
    assert car.velocity_damping == -1


def test_set_u() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    car = Car(TrackPosition(p1.connection(LEFT), 0.5))
    assert car.piece is p1
    assert car.u == 0.5
    car.u += 1
    assert car.piece is p2
    assert car.u == 0.5
    car.u -= 1
    assert car.piece is p1
    assert car.u == 0.5


def test_apply_force() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    car = Car(TrackPosition(p1.connection(LEFT), 0.5), velocity_damping=0)
    assert car.velocity == 0
    assert car.u == 0.5
    assert car.piece is p1
    car.apply_force(1)
    assert car.velocity == 0
    car.update(0, 1)
    assert car.velocity == approx(1)
    assert car.u == approx(0.5)
    assert car.piece is p2


def test_apply_impulse() -> None:
    p1, p2 = Piece.create_line(GridPosition(0, 0), RIGHT, 2)
    Grid(pieces=[p1, p2])
    car = Car(TrackPosition(p1.connection(LEFT), 0.5), velocity_damping=0)
    assert car.velocity == 0
    assert car.u == 0.5
    assert car.piece is p1
    car.apply_impulse(1)
    assert car.velocity == approx(1)


def test_constant_force_no_friction() -> None:
    c = Connection(LEFT, RIGHT)
    p = Piece(GridPosition(0, 0), connections={c})
    Grid(pieces=[p])
    car = Car(TrackPosition(p.connection(LEFT), 0), velocity_damping=0)
    last_velocity = car.velocity
    last_u = car.u
    for _ in range(10):
        car.apply_force(1)
        car.update(0, 0.01)
        assert car.velocity > last_velocity
        assert car.u > last_u
        last_velocity = car.velocity
        last_u = car.u


def test_constant_friction_no_force() -> None:
    c = Connection(LEFT, RIGHT)
    p = Piece(GridPosition(0, 0), connections={c})
    Grid(pieces=[p])
    car = Car(TrackPosition(p.connection(LEFT), 0), velocity_damping=-1)
    car.apply_impulse(1)
    last_velocity = car.velocity
    last_u = car.u
    for _ in range(10):
        car.update(0, 0.01)
        assert car.velocity < last_velocity
        assert car.u > last_u
        last_velocity = car.velocity
        last_u = car.u


def test_ends() -> None:
    p1, p2, p3 = Piece.create_line(GridPosition(0, 0), RIGHT, 3)
    Grid(pieces=[p1, p2, p3])
    car = Car(TrackPosition(p2.connection(LEFT), 0.75), length=1)
    assert car.ends == (
        TrackPosition(p2.connection(LEFT), 0.25),
        TrackPosition(p3.connection(LEFT), 0.25),
    )


def test_ends_long() -> None:
    p1, p2, p3 = Piece.create_line(GridPosition(0, 0), RIGHT, 3)
    Grid(pieces=[p1, p2, p3])
    car = Car(TrackPosition(p2.connection(LEFT), 0.5), length=2)
    assert car.ends == (
        TrackPosition(p1.connection(LEFT), 0.5),
        TrackPosition(p3.connection(LEFT), 0.5),
    )


def test_ctor_manager() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0.5)
    manager = CarManager()
    car = Car(pos, manager=manager)
    assert car.manager is manager
    assert car in manager


def test_set_manager() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0.5)
    manager = CarManager()
    car = Car(pos)
    assert car.manager is None
    assert car not in manager
    car.manager = manager
    assert car.manager is manager
    assert car in manager
    car.manager = None
    assert car.manager is None
    assert car not in manager


def test_eq() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0.5)
    car = Car(pos)
    assert car == car
    assert car != Car(pos)
    assert hash(car) == hash(car)
    assert hash(car) != hash(Car(pos))


def test_invalid_manager() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0.5)
    manager = CarManager()
    car = Car(pos, manager=manager)
    with (
        pytest.raises(Car.ValidationError),
        manager._pause_validation(),  # type:ignore
        car._pause_validation(),  # type:ignore
    ):
        manager._CarManager__cars = frozenset[Car]()  # type:ignore
