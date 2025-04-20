from tracky.cars import Car, CarManager
from tracky.sim import Sim
from tracky.track import Direction, Grid, GridPosition, Piece, TrackPosition


def test_ctor() -> None:
    grid = Grid()
    car_manager = CarManager()
    sim = Sim(grid, car_manager)
    assert sim.grid is grid
    assert sim.car_manager is car_manager


def test_eq() -> None:
    grid = Grid()
    car_manager = CarManager()
    sim = Sim(grid, car_manager)
    assert sim == sim
    assert sim != Sim(grid, car_manager)
    assert hash(sim) == hash(sim)
    assert hash(sim) != hash(Sim(grid, car_manager))


def test_update() -> None:
    p = Piece.create(GridPosition(0, 0), Direction.LEFT, Direction.RIGHT)
    grid = Grid(pieces=[p])
    car = Car(TrackPosition(p.connection(Direction.LEFT), 0), velocity_damping=0)
    car_manager = CarManager(cars=[car])
    sim = Sim(grid, car_manager)
    car.apply_impulse(1)
    sim.update(0, 0.5)
    assert car.u == 0.5
