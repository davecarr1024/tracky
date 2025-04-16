from typing import Optional

from tracky.track import Connection, Grid, GridPosition, Piece, TrackPosition


class Car:
    def __init__(
        self,
        position: TrackPosition,
        length: float = 1,
        mass: float = 1,
        velocity_damping: float = -0.1,
    ) -> None:
        self.__position = position
        self.__length = length
        self.__mass = mass
        self.__velocity: float = 0
        self.__force: float = 0
        self.__velocity_damping = velocity_damping

    @property
    def position(self) -> TrackPosition:
        return self.__position

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def u(self) -> float:
        return self.__position.u

    @u.setter
    def u(self, u: float) -> None:
        self.__position = self.__position.with_u(u)

    @property
    def connection(self) -> "Connection":
        return self.__position.connection

    @property
    def piece(self) -> Optional["Piece"]:
        return self.connection.piece

    @property
    def grid_position(self) -> Optional["GridPosition"]:
        if piece := self.piece:
            return piece.position

    @property
    def grid(self) -> Optional["Grid"]:
        if piece := self.piece:
            return piece.grid

    @property
    def length(self) -> float:
        return self.__length

    @property
    def ends(self) -> tuple[TrackPosition, TrackPosition]:
        return self.__position - self.length / 2, self.__position + self.length / 2

    @property
    def mass(self) -> float:
        return self.__mass

    @property
    def velocity_damping(self) -> float:
        return self.__velocity_damping

    def advance(self, du: float) -> None:
        self.__position += du

    def apply_impulse(self, impulse: float) -> None:
        self.__velocity += impulse / self.__mass

    def apply_force(self, force: float) -> None:
        """Apply a per-second force to the car.

        Note that this is a per-second force, not a per-frame force. Force is
        accumulated each frame and applied as an instantaneous impulse at the end of the
        frame. To apply a total of n units of force, call this method every fram for
        1 second with force=n.
        """
        self.__force += force

    def update(self, t: float, dt: float) -> None:
        # Apply velocity damping as a friction-like force.
        self.apply_force(self.__velocity * self.__velocity_damping)
        # Apply accumulated force as an impulse.
        self.apply_impulse(self.__force * dt)
        self.__force = 0
        self.advance(self.__velocity * dt)
