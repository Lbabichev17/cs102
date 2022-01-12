import copy
import pathlib
import random
import typing as tp
from copy import deepcopy
from pprint import pprint as pp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            current = []
            for j in range(self.cols):
                current.append(random.randint(0, 1) if randomize else 0)
            grid.append(current)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        x, y = cell[0], cell[1]
        if x >= 1:
            neighbours.append(self.curr_generation[x - 1][y])
        if x + 1 < self.rows:
            neighbours.append(self.curr_generation[x + 1][y])
        if y >= 1:
            neighbours.append(self.curr_generation[x][y - 1])
        if y + 1 < self.cols:
            neighbours.append(self.curr_generation[x][y + 1])
        if x >= 1 and y >= 1:
            neighbours.append(self.curr_generation[x - 1][y - 1])
        if x >= 1 and y + 1 < self.cols:
            neighbours.append(self.curr_generation[x - 1][y + 1])
        if x + 1 < self.rows and y >= 1:
            neighbours.append(self.curr_generation[x + 1][y - 1])
        if x + 1 < self.rows and y + 1 < self.cols:
            neighbours.append(self.curr_generation[x + 1][y + 1])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_gen = copy.deepcopy(self.curr_generation)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)
                summ_of_neighbours = sum(self.get_neighbours(cell))
                if summ_of_neighbours < 2 or summ_of_neighbours > 3:
                    new_gen[row][col] = 0
                elif summ_of_neighbours == 3:
                    new_gen[row][col] = 1
        return new_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        curr_gen = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if len(line) > 1:
                    curr_gen.append(list(map(int, line[0:-1])))
        life = GameOfLife((len(curr_gen), len(curr_gen[0])))
        life.curr_generation = curr_gen
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for i, rows in enumerate(self.curr_generation):
                for j, elem in enumerate(rows):
                    f.write(str(elem))
                f.write("\n")


if __name__ == "__main__":
    life = GameOfLife.from_file(pathlib.Path("glider.txt"))
    pp(life.curr_generation)
    for _ in range(4):
        pp(life.prev_generation)
        pp(life.curr_generation)
        life.step()
