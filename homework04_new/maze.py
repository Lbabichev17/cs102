from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    currenty, currentx = coord
    cols = len(grid[0])
    direction = randint(0, 1)
    if direction == 0:
        if currenty == 1:
            if currentx != cols - 2:
                grid[currenty][currentx + 1] = " "
        else:
            grid[currenty - 1][currentx] = " "
    else:
        if currentx != cols - 2:
            grid[currenty][currentx + 1] = " "
        else:
            if currenty != 1:
                grid[currenty - 1][currentx] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    if random_exit:
        start = (0, randint(0, rows - 1))
        end = (randint(0, rows - 1), 0)
    else:
        start = (0, rows - 1)
        end = (cols - 1, 0)

    # задать начало и конец сетки с помощью Х
    grid[start[0]][start[1]] = "X"
    grid[end[0]][end[1]] = "X"

    for currenty in range(1, rows, 2):
        for currentx in range(1, cols, 2):
            direction = randint(0, 1)
            if direction == 0:
                if currenty == 1:
                    if currentx != cols - 2:
                        grid[currenty][currentx + 1] = " "
                else:
                    grid[currenty - 1][currentx] = " "
            else:
                if currentx != cols - 2:
                    grid[currenty][currentx + 1] = " "
                else:
                    if currenty != 1:
                        grid[currenty - 1][currentx] = " "

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    list1 = []
    for y in range(len(grid)):
        if "X" == grid[y][0]:
            list1.append((y, 0))
    for x in range(len(grid)):
        if "X" == grid[0][x]:
            list1.append((0, x))
    return sorted(list1)


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == k:
                if grid[row + 1][col] == 0:
                    grid[row + 1][col] = k + 1
                if grid[row - 1][col] == 0:
                    grid[row - 1][col] = k + 1
                if grid[row][col + 1] == 0:
                    grid[row][col + 1] = k + 1
                if grid[row][col - 1] == 0:
                    grid[row][col - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    """
    3. По полученной разметке ищем путь домой:
        1. запрыгиваем в клетку выхода
        2. пока не придем в клетку входа (пока не найдем 1):
            1. если в одной из соседних с текущей клеток лежит значение, на один меньшее текущего k (длины пути), записываем в путь координаты найденной клетки, уменьшаем счетчик k на 1
            2. переходим в следующую клетку, направление задает только что найденная клетка
        3. если длина пути (списка координат) не равна длине пути, записанной в клетке выхода
            1. отпрыгиваем на клетку пути назад
            2. заполняем неудачную клетку пробелом, чтобы никогда больше в нее не вернуться
            3. рекурсивно повторяем пункт 3, пока не найдем путь (ситуация, когда его нет, к этому моменту уже исключена)
    """
    path = [exit_coord]
    currentcoord = exit_coord
    k = int(grid[currentcoord[0]][currentcoord[1]])
    (row, col) = currentcoord
    if currentcoord[0] != len(grid) - 1:
        if grid[row + 1][col] == k - 1:
            currentcoord = (row + 1, col)
            path.append(currentcoord)
            k -= 1
    if currentcoord[0] != 0:
        if grid[row - 1][col] == k - 1:
            currentcoord = (row - 1, col)
            path.append(currentcoord)
            k -= 1
    if currentcoord[1] != len(grid[0]) - 1:
        if grid[row][col + 1] == k - 1:
            currentcoord = (row, col + 1)
            path.append(currentcoord)
            k -= 1
    if currentcoord[1] != 0:
        if grid[row][col - 1] == k - 1:
            currentcoord = (row, col - 1)
            path.append(currentcoord)
            k -= 1
    while grid[currentcoord[0]][currentcoord[1]] != 1:
        (row, col) = currentcoord
        if grid[row + 1][col] == k - 1:
            currentcoord = (row + 1, col)
            path.append(currentcoord)
            k -= 1
        elif grid[row - 1][col] == k - 1:
            currentcoord = (row - 1, col)
            path.append(currentcoord)
            k -= 1
        elif grid[row][col + 1] == k - 1:
            currentcoord = (row, col + 1)
            path.append(currentcoord)
            k -= 1
        elif grid[row][col - 1] == k - 1:
            currentcoord = (row, col - 1)
            path.append(currentcoord)
            k -= 1

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    1. дверь попала на один из углов и окружена с двух сторон → возвращаем `True`
    2. дверь попала на одну из стенок и окружена с трех сторон → возвращаем `True`
    3. клетка лежит на одной из стенок и окружена с двух сторон, проход к следующей пустой есть → возвращаем `False`
    """
    # проверяем первое условие
    if (
        coord == (0, 0)
        or coord == (0, len(grid) - 1)
        or coord == (len(grid[0]) - 1, 0)
        or coord == (len(grid[0]) - 1, len(grid) - 1)
    ):
        return True

    if coord[1] == 0:
        if grid[coord[0]][coord[1] + 1] == "■":
            return True
    if coord[0] == 0:
        if grid[coord[0] + 1][coord[1]] == "■":
            return True
    if coord[0] == len(grid) - 1:
        if grid[coord[0] - 1][coord[1]] == "■":
            return True
    if coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][coord[1] - 1] == "■":
            return True
    return False


def solve_maze(grid: List[List[Union[str, int]]]) -> Optional[List[Tuple[int, int]]]:
    exits = get_exits(grid)
    if len(exits) == 1:
        return None

    for i in exits:
        if encircled_exit(grid, i):
            return None
    start = exits[0]
    end = exits[1]

    grid[start[0]][start[1]] = 1
    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == " ":
                grid[row][col] = 0

    grid[end[0]][end[1]] = 0

    k = 1
    if start[0] != len(grid) - 1:
        if grid[start[0] + 1][start[1]] == 0:
            grid[start[0] + 1][start[1]] = k + 1
    if start[0] != 0:
        if grid[start[0] - 1][start[1]] == 0:
            grid[start[0] - 1][start[1]] = k + 1
    if start[1] != len(grid[0]) - 1:
        if grid[start[0]][start[1] + 1] == 0:
            grid[start[0]][start[1] + 1] = k + 1
    if start[1] != 0:
        if grid[start[0]][start[1] - 1] == 0:
            grid[start[0]][start[1] - 1] = k + 1
    while grid[end[0]][end[1]] == 0:
        k += 1
        make_step(grid, k)
    return shortest_path(grid, end)


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    grid1 = [row[:] for row in GRID]
    path1 = solve_maze(grid1)
    MAZE = add_path_to_grid(GRID, path1)
    print(pd.DataFrame(MAZE))