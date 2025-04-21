import functools
import math
from dataclasses import dataclass
from typing import Optional

from tracky.core import Errorable
from tracky.track import Connection, ConnectionShape, Direction, GridPosition, TrackPosition
from tracky.visuals.rectangle import Rectangle
from tracky.visuals.vector import Vector


@dataclass(frozen=True)
class Projection(Errorable):
    """Projection of game grid space to screen space."""

    screen_rect: Rectangle
    grid_origin: GridPosition
    tile_size: int

    @property
    def grid_num_cols(self) -> int:
        return self.screen_rect.width // self.tile_size

    @property
    def grid_num_rows(self) -> int:
        return self.screen_rect.height // self.tile_size

    @property
    def grid_max(self) -> GridPosition:
        return GridPosition(
            row=self.grid_origin.row + self.grid_num_rows,
            col=self.grid_origin.col + self.grid_num_cols,
        )

    def grid_to_screen(self, position: GridPosition) -> Optional[Vector]:
        result = self.screen_rect.min + Vector(
            (position.col - self.grid_origin.col) * self.tile_size,
            (position.row - self.grid_origin.row) * self.tile_size,
        )
        if result in self.screen_rect:
            return result

    def screen_to_grid(self, position: Vector) -> Optional[GridPosition]:
        if position in self.screen_rect:
            rel = (position - self.screen_rect.min) // self.tile_size
            return GridPosition(row=rel.y + self.grid_origin.row, col=rel.x + self.grid_origin.col)

    def tile_center(self, position: GridPosition) -> Optional[Vector]:
        if pos := self.grid_to_screen(position):
            return pos + Vector(self.tile_size // 2, self.tile_size // 2)

    def tile_side(self, position: GridPosition, direction: Direction) -> Optional[Vector]:
        if pos := self.grid_to_screen(position):
            match direction:
                case Direction.LEFT:
                    return pos + Vector(0, self.tile_size // 2)
                case Direction.UP:
                    return pos + Vector(self.tile_size // 2, 0)
                case Direction.RIGHT:
                    return pos + Vector(self.tile_size, self.tile_size // 2)
                case Direction.DOWN:
                    return pos + Vector(self.tile_size // 2, self.tile_size)

    def tile_corner(
        self, position: GridPosition, directions: tuple[Direction, Direction]
    ) -> Optional[Vector]:
        if pos := self.grid_to_screen(position):
            match directions:
                case (Direction.UP, Direction.LEFT) | (Direction.LEFT, Direction.UP):
                    return pos
                case (Direction.UP, Direction.RIGHT) | (Direction.RIGHT, Direction.UP):
                    return pos + Vector(self.tile_size, 0)
                case (Direction.DOWN, Direction.LEFT) | (Direction.LEFT, Direction.DOWN):
                    return pos + Vector(0, self.tile_size)
                case (Direction.DOWN, Direction.RIGHT) | (Direction.RIGHT, Direction.DOWN):
                    return pos + Vector(self.tile_size, self.tile_size)
                case _:
                    return None

    def connection_ends(self, connection: Connection) -> Optional[tuple[Vector, Vector]]:
        if (
            (position := connection.position)
            and (reverse_side := self.tile_side(position, connection.reverse_direction))
            and (forward_side := self.tile_side(position, connection.forward_direction))
        ):
            return reverse_side, forward_side

    def connection_corner(self, connection: Connection) -> Optional[Vector]:
        if position := connection.position:
            return self.tile_corner(
                position,
                (
                    connection.reverse_direction,
                    connection.forward_direction,
                ),
            )

    def connection_lerp(self, connection: Connection, u: float) -> Optional[Vector]:
        if (ends := self.connection_ends(connection)) and (
            connection_shape := connection.connection_shape
        ):
            reverse_pos, forward_pos = ends
            match connection_shape:
                case ConnectionShape.STRAIGHT:
                    return reverse_pos.lerp(forward_pos, u)
                case ConnectionShape.CURVED:
                    if corner := self.connection_corner(connection):

                        @functools.cache
                        def angles(
                            reverse_delta: Vector, forward_delta: Vector
                        ) -> tuple[float, float]:
                            return (
                                math.atan2(reverse_delta.y, reverse_delta.x),
                                math.atan2(forward_delta.y, forward_delta.x),
                            )

                        # This piece curves around corner - find angles from corner to sides.
                        reverse_th, forward_th = angles(
                            (reverse_pos - corner).norm(),
                            (forward_pos - corner).norm(),
                        )
                        # Fix forward_th to be in the same rotation as reverse_th.
                        delta_th = (forward_th - reverse_th + math.pi * 3) % (math.pi * 2) - math.pi
                        # Lerp the between the two rotations.
                        th = reverse_th + delta_th * u
                        # Use lerped the to find lerped pos along curved path.
                        return corner + Vector(
                            int(math.cos(th) * self.tile_size / 2),
                            int(math.sin(th) * self.tile_size / 2),
                        )
                    else:
                        # No corner found between sides - this is a straight piece of track.
                        return reverse_pos.lerp(forward_pos, u)

    def track_to_screen(self, track_position: TrackPosition) -> Optional[Vector]:
        return self.connection_lerp(track_position.connection, track_position.u)
