from tracky.track import TrackPosition


class Car:
    def __init__(
        self,
        position: TrackPosition,
        length: float = 1,
        mass: float = 1,
    ) -> None:
        self.__position = position
        self.__length = length
        self.__mass = mass
        self.__velocity: float = 0
        self.__force: float = 0

    @property
    def position(self) -> TrackPosition:
        return self.__position

    @property
    def length(self) -> float:
        return self.__length

    @property
    def mass(self) -> float:
        return self.__mass

    def advance(self, du: float) -> None:
        self.__position += du

    def apply_impulse(self, impulse: float) -> None:
        self.__velocity += impulse / self.__mass

    def apply_force(self, force: float) -> None:
        self.__force += force

    def update(self, t: float, dt: float) -> None:
        acceleration = self.__force / self.__mass * dt
        self.__force = 0
        self.__velocity += acceleration * dt
        self.advance(self.__velocity * dt)
