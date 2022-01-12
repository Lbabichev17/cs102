import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []
        for i in range(self.cell_height):
            current = []
            for j in range(self.cell_width):
                current.append(random.randint(0, 1) if randomize else 0)
            grid.append(current)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0
        for row in self.grid:
            x = 0
            for cell in row:
                color = pygame.Color("green") if cell else pygame.Color("white")
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        x = cell[0] // self.cell_size
        y = cell[1] // self.cell_size
        if x >= 1:
            neighbours.append(self.grid[x - 1][y])
        if x + 1 < self.cell_height:
            neighbours.append(self.grid[x + 1][y])
        if y >= 1:
            neighbours.append(self.grid[x][y - 1])
        if y + 1 < self.cell_width:
            neighbours.append(self.grid[x][y + 1])
        if x >= 1 and y >= 1:
            neighbours.append(self.grid[x - 1][y - 1])
        if x >= 1 and y + 1 < self.cell_width:
            neighbours.append(self.grid[x - 1][y + 1])
        if x + 1 < self.cell_height and y >= 1:
            neighbours.append(self.grid[x + 1][y - 1])
        if x + 1 < self.cell_height and y + 1 < self.cell_width:
            neighbours.append(self.grid[x + 1][y + 1])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_gen = copy.deepcopy(self.grid)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                cell = (row, col)
                summ_of_neighbours = sum(self.get_neighbours(cell))
                if self.grid[row][col] == 1:
                    if summ_of_neighbours == 3 or summ_of_neighbours == 2:
                        new_gen[row][col] = 1
                    else:
                        new_gen[row][col] = 0
                else:
                    if summ_of_neighbours == 3:
                        new_gen[row][col] = 1
                    else:
                        new_gen[row][col] = 0
        return new_gen


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
