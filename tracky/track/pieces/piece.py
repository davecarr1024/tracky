from collections import defaultdict
from typing import Iterable, Mapping, Optional, override

from tracky.core import Error, Validatable
from tracky.track.grid.direction import Direction
from tracky.track.grid.position import Position
from tracky.track.pieces.connection import Connection


class Piece(Validatable):
    class KeyError(Error, KeyError): ...

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
    def __repr__(self) -> str:
        return f"Piece(position={self.__position}, connections={self.__connections})"

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
            connections_by_direction[connection.reverse_direction].add(connection)
        for direction, connections in connections_by_direction.items():
            if len(connections) > 1:
                raise self._validation_error(
                    f"multiple connections in direction {direction}: {connections}"
                )

    @property
    def connections_by_direction(self) -> Mapping[Direction, Connection]:
        return {connection.reverse_direction: connection for connection in self.connections}

    def connection(self, direction: Direction) -> Connection:
        try:
            return self.connections_by_direction[direction]
        except KeyError as e:
            raise self.KeyError(f"no connection for direction {direction} in piece {self}") from e

    def reverse_position(self, direction: Direction) -> Optional[Position]:
        if connection := self.connection(direction):
            return self.position + connection.reverse_direction

    def _piece(self, position: Position) -> Optional["Piece"]:
        return self.__grid.get(position) if self.__grid is not None else None

    def reverse_piece(self, direction: Direction) -> Optional["Piece"]:
        if position := self.reverse_position(direction):
            return self._piece(position)

    def forward_position(self, direction: Direction) -> Optional[Position]:
        if connection := self.connection(direction):
            return self.position + connection.forward_direction

    def forward_piece(self, direction: Direction) -> Optional["Piece"]:
        if position := self.forward_position(direction):
            return self._piece(position)

    @staticmethod
    def create(
        position: Position,
        reverse_direction: Direction,
        forward_direction: Direction,
    ) -> "Piece":
        return Piece(
            position=position,
            connections=[
                Connection(
                    reverse_direction=reverse_direction,
                    forward_direction=forward_direction,
                ),
                Connection(
                    reverse_direction=forward_direction,
                    forward_direction=reverse_direction,
                ),
            ],
        )

    @staticmethod
    def create_line(
        position: Position,
        direction: Direction,
        length: int,
    ) -> Iterable["Piece"]:
        for _ in range(length):
            yield Piece.create(
                position=position,
                reverse_direction=-direction,
                forward_direction=direction,
            )
            position += direction


from tracky.track.grid import grid
