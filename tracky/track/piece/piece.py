from collections import defaultdict
from typing import Iterable, Mapping, Optional, override

from tracky.core import Validatable
from tracky.track.grid.direction import Direction
from tracky.track.grid.position import Position
from tracky.track.piece.connection import Connection


class Piece(Validatable):
    def __init__(
        self,
        position: Position,
        connections: Optional[Iterable[Connection]] = None,
        grid: Optional["grid.Grid"] = None,
    ) -> None:
        super().__init__()
        self.__grid: Optional["grid.Grid"] = None
        self.__connections = frozenset[Connection]()
        with self._pause_validation():
            self.__position = position
            if connections is not None:
                self.connections = frozenset(connections)
            self.grid = grid

    @override
    def __eq__(self, other: object) -> bool:
        return other is self

    @override
    def __hash__(self) -> int:
        return id(self)

    @property
    def position(self) -> Position:
        return self.__position

    @property
    def connections(self) -> frozenset[Connection]:
        return self.__connections

    @connections.setter
    def connections(self, connections: Iterable[Connection]) -> None:
        connections_ = frozenset(connections)
        if connections_ != self.__connections:
            with self._pause_validation():
                added_connections = connections_ - self.__connections
                removed_connections = self.__connections - connections_
                self.__connections = connections_
                for connection in added_connections:
                    connection.piece = self
                for connection in removed_connections:
                    connection.piece = None

    def add_connection(self, connection: Connection) -> None:
        self.connections |= {connection}

    def remove_connection(self, connection: Connection) -> None:
        self.connections -= {connection}

    @property
    def grid(self) -> Optional["grid.Grid"]:
        return self.__grid

    @grid.setter
    def grid(self, grid: Optional["grid.Grid"]) -> None:
        if grid != self.__grid:
            with self._pause_validation():
                if self.__grid is not None:
                    self.__grid.remove_piece(self)
                self.__grid = grid
                if self.__grid is not None:
                    self.__grid.add_piece(self)

    def _validate(self) -> None:
        if self.__grid is not None and self not in self.__grid.pieces:
            raise self._validation_error(f"not in grid {self.__grid}")
        connections_by_direction = defaultdict[Direction, set[Connection]](set)
        for connection in self.connections:
            connections_by_direction[connection.from_direction].add(connection)
        for direction, connections in connections_by_direction.items():
            if len(connections) > 1:
                raise self._validation_error(
                    f"multiple connections in direction {direction}: {connections}"
                )

    @property
    def connections_by_from_direction(self) -> Mapping[Direction, Connection]:
        return {
            connection.from_direction: connection for connection in self.connections
        }

    def connection_for_from_direction(
        self, direction: Direction
    ) -> Optional[Connection]:
        return self.connections_by_from_direction.get(direction)

    def last_position_for_from_direction(
        self, direction: Direction
    ) -> Optional[Position]:
        if connection := self.connection_for_from_direction(direction):
            return self.position + connection.from_direction

    def _piece(self, position: Position) -> Optional["Piece"]:
        return self.__grid.get(position) if self.__grid is not None else None

    def last_piece_for_from_direction(self, direction: Direction) -> Optional["Piece"]:
        if position := self.last_position_for_from_direction(direction):
            return self._piece(position)

    def next_position_for_from_direction(
        self, direction: Direction
    ) -> Optional[Position]:
        if connection := self.connection_for_from_direction(direction):
            return self.position + connection.to_direction

    def next_piece_for_from_direction(self, direction: Direction) -> Optional["Piece"]:
        if position := self.next_position_for_from_direction(direction):
            return self._piece(position)


from tracky.track.grid import grid
