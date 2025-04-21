from dataclasses import dataclass
from typing import Optional, SupportsFloat

from tracky.core import Errorable
from tracky.track import Connection, ConnectionShape, Direction, GridPosition, TrackPosition
from tracky.visuals.offset import Offset
from tracky.visuals.position import Position
from tracky.visuals.rectangle import Rectangle
from tracky.visuals.rotation import Rotation


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

    def grid_to_screen(self, position: GridPosition) -> Optional[Position]:
        result = (
            self.screen_rect.min
            + Offset(
                (position.col - self.grid_origin.col),
                (position.row - self.grid_origin.row),
            )
            * self.tile_size
        )
        if result in self.screen_rect:
            return result

    def screen_to_grid(self, position: Position) -> Optional[GridPosition]:
        if position in self.screen_rect:
            rel = (position - self.screen_rect.min) // self.tile_size
            return GridPosition(
                row=rel.dy + self.grid_origin.row, col=rel.dx + self.grid_origin.col
            )

    def tile_center(self, position: GridPosition) -> Optional[Position]:
        if pos := self.grid_to_screen(position):
            return pos + Offset(self.tile_size // 2, self.tile_size // 2)

    def tile_side(self, position: GridPosition, direction: Direction) -> Optional[Position]:
        if pos := self.grid_to_screen(position):
            match direction:
                case Direction.LEFT:
                    return pos + Offset(0, self.tile_size // 2)
                case Direction.UP:
                    return pos + Offset(self.tile_size // 2, 0)
                case Direction.RIGHT:
                    return pos + Offset(self.tile_size, self.tile_size // 2)
                case Direction.DOWN:
                    return pos + Offset(self.tile_size // 2, self.tile_size)

    def tile_corner(
        self, position: GridPosition, directions: tuple[Direction, Direction]
    ) -> Optional[Position]:
        if pos := self.grid_to_screen(position):
            match directions:
                case (Direction.UP, Direction.LEFT) | (Direction.LEFT, Direction.UP):
                    return pos
                case (Direction.UP, Direction.RIGHT) | (Direction.RIGHT, Direction.UP):
                    return pos + Offset(self.tile_size, 0)
                case (Direction.DOWN, Direction.LEFT) | (Direction.LEFT, Direction.DOWN):
                    return pos + Offset(0, self.tile_size)
                case (Direction.DOWN, Direction.RIGHT) | (Direction.RIGHT, Direction.DOWN):
                    return pos + Offset(self.tile_size, self.tile_size)
                case _:
                    return None

    def connection_ends(self, connection: Connection) -> Optional[tuple[Position, Position]]:
        if (
            (position := connection.position)
            and (reverse_side := self.tile_side(position, connection.reverse_direction))
            and (forward_side := self.tile_side(position, connection.forward_direction))
        ):
            return reverse_side, forward_side

    def connection_corner(self, connection: Connection) -> Optional[Position]:
        if position := connection.position:
            return self.tile_corner(
                position,
                (
                    connection.reverse_direction,
                    connection.forward_direction,
                ),
            )

    def connection_lerp(
        self,
        connection: Connection,
        u: SupportsFloat,
    ) -> Optional[tuple[Position, Rotation]]:
        print(f"\nconnection_lerp: c: {connection}, u: {u}")
        if (ends := self.connection_ends(connection)) and (
            connection_shape := connection.connection_shape
        ):
            reverse_pos, forward_pos = ends
            print(
                f"reverse_pos: {reverse_pos}, "
                f"forward_pos: {forward_pos}, "
                f"connection_shape: {connection_shape}"
            )
            match connection_shape:
                case ConnectionShape.STRAIGHT:
                    return (
                        reverse_pos.lerp(forward_pos, u),
                        reverse_pos.direction_to(forward_pos),
                    )
                case ConnectionShape.CURVED:
                    if corner := self.connection_corner(connection):
                        print(f"corner: {corner}")
                        # Diffs from entry and exit positions to corner.
                        reverse_diff = reverse_pos - corner
                        forward_diff = forward_pos - corner
                        print(f"reverse_diff: {reverse_diff}, " f"forward_diff: {forward_diff}")
                        # Rotations about corner to entry and exit positions.
                        reverse_rotation = reverse_diff.as_rotation()
                        forward_rotation = forward_diff.as_rotation()
                        print(
                            f"reverse_rotation: {reverse_rotation}, "
                            f"forward_rotation: {forward_rotation}"
                        )
                        # Lerp u between rotations to get rotation about corner.
                        corner_rotation = reverse_rotation.lerp(forward_rotation, u)
                        print(f"corner_rotation: {corner_rotation}")
                        # Apply that rotation to the entry diff to get the position
                        # relative to the tile, and add that to the corner to get
                        # the position on the screen.
                        position = corner + corner_rotation * Offset(int(reverse_diff.length), 0)
                        print(f"position: {position}")

                        # Get the direction of travel at entry and exit points.
                        entry_direction = -connection.reverse_direction
                        exit_direction = connection.forward_direction
                        # Get the rotations of those directions.
                        entry_rotation = Rotation.from_direction(entry_direction)
                        exit_rotation = Rotation.from_direction(exit_direction)
                        # The final rotation is the lerp between the entry and
                        # exit rotations.
                        rotation = entry_rotation.lerp(exit_rotation, u)

                        return position, rotation
                    else:
                        # No corner found between sides - this is a straight piece of track.
                        return (
                            reverse_pos.lerp(forward_pos, u),
                            reverse_pos.direction_to(forward_pos),
                        )

    def track_to_screen(self, track_position: TrackPosition) -> Optional[tuple[Position, Rotation]]:
        return self.connection_lerp(track_position.connection, track_position.u)
