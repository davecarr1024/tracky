import pytest
from pytest import approx  # type: ignore

from tracky.cars import Car, CarManager
from tracky.track import LEFT, RIGHT, Grid, GridPosition, Piece, TrackPosition


def test_ctor_empty() -> None:
    manager = CarManager()
    assert manager.cars == set()
    assert set(manager) == set()


def test_ctor_cars() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0)
    car = Car(pos)
    manager = CarManager(cars=[car])
    assert manager.cars == {car}
    assert set(manager) == {car}
    assert car.manager is manager


def test_eq() -> None:
    manager = CarManager()
    assert manager == manager
    assert manager != CarManager()
    assert hash(manager) == hash(manager)
    assert hash(manager) != hash(CarManager())


def test_set_cars() -> None:
    manager = CarManager()
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0)
    car = Car(pos)
    assert manager.cars == set()
    assert car.manager is None
    manager.cars = {car}
    assert manager.cars == {car}
    assert car.manager is manager
    manager.cars = set()
    assert manager.cars == set()
    assert car.manager is None


def test_update() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0)
    car = Car(pos, velocity_damping=0)
    manager = CarManager(cars=[car])
    assert car.u == 0
    car.apply_impulse(1)
    manager.update(0, 0.5)
    assert car.u == approx(0.5)


def test_invalid_car() -> None:
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0)
    car = Car(pos)
    manager = CarManager(cars=[car])
    with (
        pytest.raises(CarManager.ValidationError),
        manager._pause_validation(),  # type:ignore
        car._pause_validation(),  # type:ignore
    ):
        car._Car__manager = None  # type:ignore


def test_len() -> None:
    manager = CarManager()
    assert len(manager) == 0
    p = Piece.create(GridPosition(0, 0), LEFT, RIGHT)
    Grid(pieces=[p])
    pos = TrackPosition(p.connection(LEFT), 0)
    car = Car(pos)
    manager.add_car(car)
    assert len(manager) == 1
    manager.remove_car(car)
    assert len(manager) == 0
