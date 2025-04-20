# coverage: skip file

from dataclasses import dataclass
from typing import Optional

import pygame

from tracky.sim import Sim
from tracky.track import Grid, GridPosition, Piece


@dataclass(frozen=True)
class Vec:
    x: int
    y: int


@dataclass(frozen=True)
class Rect:
    min: Vec
    max: Vec


class Visualizer:
    def __init__(
        self,
        sim: Sim,
        size: Optional[Vec] = None,
        title: str = "tracky",
        fps: int = 60,
    ) -> None:
        self.__sim = sim
        self.__size = size or Vec(800, 600)
        self.__title = title
        self.__fps = fps

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.__size.x, self.__size.y))
        pygame.display.set_caption(self.__title)
        clock = pygame.time.Clock()
        t = 0.0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            dt = clock.tick(self.__fps) / 1000
            t += dt
            self._update(t, dt)

            screen.fill((0, 0, 200))
            self._render()
            pygame.display.flip()

    def _update(self, t: float, dt: float) -> None:
        self.__sim.update(t, dt)

    def _render(self) -> None:
        self._render_sim(self.__sim, Rect(Vec(0, 0), self.__size))

    def _render_sim(self, sim: Sim, rect: Rect) -> None:
        self._render_grid(sim.grid, rect)

    def _render_grid(self, grid: Grid, rect: Rect) -> None:
        min_pos, max_pos = grid.bounds
        grid_num_rows = max_pos.row - min_pos.row + 1
        grid_num_cols = max_pos.col - min_pos.col + 1
        cell_width: int = int((rect.max.x - rect.min.x) / grid_num_cols)
        cell_height: int = int((rect.max.y - rect.min.y) / grid_num_rows)
        for row in range(min_pos.row, max_pos.row + 1):
            for col in range(min_pos.col, max_pos.col + 1):
                if piece := grid.get(GridPosition(row, col)):
                    self._render_piece(
                        piece,
                        Rect(
                            min=Vec(
                                x=rect.min.x + col * cell_width,
                                y=rect.min.y + row * cell_height,
                            ),
                            max=Vec(
                                x=rect.min.x + (col + 1) * cell_width,
                                y=rect.min.y + (row + 1) * cell_height,
                            ),
                        ),
                    )

    def _render_piece(self, piece: Piece, rect: Rect) -> None: ...
