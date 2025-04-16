from typing import override

from tracky.cars import CarManager
from tracky.track import Grid


class Sim:
    def __init__(self, grid: Grid, car_manager: CarManager) -> None:
        self.__grid = grid
        self.__car_manager = car_manager

    @property
    def grid(self) -> Grid:
        return self.__grid

    @property
    def car_manager(self) -> CarManager:
        return self.__car_manager

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @override
    def __repr__(self) -> str:
        return f"Sim(grid={self.grid}, car_manager={self.car_manager})"

    def update(self, t: float, dt: float) -> None:
        self.car_manager.update(t, dt)
