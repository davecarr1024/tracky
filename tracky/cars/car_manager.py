from collections.abc import Set
from typing import Iterable, Iterator, Optional, override

from tracky.core import Validatable


class CarManager(Validatable, Set["car.Car"]):
    def __init__(self, cars: Optional[Iterable["car.Car"]] = None) -> None:
        Validatable.__init__(self)
        self.__cars = frozenset[car.Car]()
        with self._pause_validation():
            if cars is not None:
                self.cars = frozenset(cars)

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @override
    def __repr__(self) -> str:
        return f"CarManager(cars={self.__cars})"

    @property
    def cars(self) -> frozenset["car.Car"]:
        return self.__cars

    @cars.setter
    def cars(self, cars: Iterable["car.Car"]) -> None:
        cars_ = frozenset(cars)
        if cars_ != self.__cars:
            with self._pause_validation():
                added_cars = cars_ - self.__cars
                removed_cars = self.__cars - cars_
                self.__cars = cars_
                for car in added_cars:
                    car.manager = self
                for car in removed_cars:
                    car.manager = None

    def add_car(self, car: "car.Car") -> None:
        self.cars |= {car}

    def remove_car(self, car: "car.Car") -> None:
        self.cars -= {car}

    def update(self, t: float, dt: float) -> None:
        for car_ in self.cars:
            car_.update(t, dt)

    @override
    def _validate(self) -> None:
        for car_ in self.__cars:
            if car_.manager != self:
                raise self._validation_error(f"car {car_} not in manager")

    @override
    def __len__(self) -> int:
        return len(self.__cars)

    @override
    def __iter__(self) -> Iterator["car.Car"]:
        return iter(self.__cars)

    @override
    def __contains__(self, car: object) -> bool:
        return car in self.__cars


from tracky.cars import car
