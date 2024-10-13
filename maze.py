import heapq
from math import sqrt
from typing import Dict
from collections import defaultdict, deque
from random import choices, shuffle, uniform
from time import sleep

from primitives import Cell, Point
from window import Window


# flattened directions array: down, right, up, left
DIRECTIONS = [0, 1, 0, -1, 0]
DOWN, RIGHT, UP, LEFT = 0, 1, 2, 3

class Maze:
    """
    The `Maze` object stores a matrix of cells that connect to one another to
    form a maze with at least one valid path from the top left corner to the
    bottom right corner.

    Attributes:
        num_cols(int): The number of columns in the maze
        num_rows(int): The number of rows in the maze
        cell_width(int): The pixel width of each maze cell
        cell_height(int): The pixel height of each maze cell
        delay(int): The minimum time to wait after calling the _animate method
        win(int): The `Window` object
        prob(float): The probability of a random wall being broken for each cell
        cells(List[List[Cell]]): The matrix of cells that make up the maze
    """

    def __init__(
        self,
        num_cols: int,
        num_rows: int,
        cell_width: int,
        cell_height: int,
        delay: int,
        prob: float,
        win: Window,
    ):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.win = win
        self.delay = delay
        self.prob = prob
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls()
        self.clear_cell_states()

    def clear_cell_states(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def _create_cells(self):
        self.cells = [[None] * self.num_rows for _ in range(self.num_cols)]
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.cells[col][row] = Cell(
                    Point(col * self.cell_width, row * self.cell_height),
                    self.cell_width,
                    self.cell_height,
                )

    def _draw_cell(self, col: int, row: int):
        self.win.draw_cell(self.cells[col][row])

    def _animate(self):
        self.win.redraw()
        if self.delay > 0:
            sleep(self.delay)

    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top = False
        self.cells[-1][-1].has_bottom = False

    def _break_up(self, i: int, j: int):
        self.cells[i][j].has_top = False
        self.cells[i][j - 1].has_bottom = False

    def _break_down(self, i: int, j: int):
        self.cells[i][j].has_bottom = False
        self.cells[i][j + 1].has_top = False

    def _break_left(self, i: int, j: int):
        self.cells[i][j].has_left = False
        self.cells[i - 1][j].has_right = False

    def _break_right(self, i: int, j: int):
        self.cells[i][j].has_right = False
        self.cells[i + 1][j].has_left = False

    def _break_direction(self, i: int, j: int, direction: int):
        if direction == DOWN:
            self._break_down(i, j)
        elif direction == RIGHT:
            self._break_right(i, j)
        elif direction == UP:
            self._break_up(i, j)
        else: # direction == LEFT
            self._break_left(i, j)
        
    def _break_walls(self):
        stack = [(0, 0)]

        while stack:
            i, j = stack.pop()
            self.cells[i][j].visited = True
            directions = list(range(4))
            shuffle(directions)
            for k in directions:
                ni, nj = i + DIRECTIONS[k], j + DIRECTIONS[k + 1]
                if self._is_unvisited(ni, nj):
                    stack.append((i, j))
                    stack.append((ni, nj))
                    self._break_direction(i, j, k)
                    break

        # randomly break walls based on self.prob probability
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                if uniform(0, 1) > self.prob:
                    continue
                dirs = []
                for k in range(4):
                    ni, nj = i + DIRECTIONS[k], j + DIRECTIONS[k + 1]
                    if 0 <= ni < self.num_cols-1 and 0 <= nj < self.num_rows-1 and not self._blocked(i, j, k):
                        dirs.append(k)
                if len(dirs) > 0:
                    self._break_direction(i, j, choices(dirs))

    def draw(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self._draw_cell(col, row)

    def solve(self, algorithm: str = "dfs") -> bool:
        if algorithm == "dfs":
            return self._solve_dfs()
        elif algorithm == "bfs":
            return self._solve_bfs()
        elif algorithm == "astar":
            return self._solve_a_star()

        return False

    def _solve_dfs(self):
        stack = [(0, 0)]
        parents = {}

        while stack:
            self._animate()
            i, j = stack.pop()
            self.cells[i][j].visited = True
            self._draw_cell(i, j)
            parent = parents.get((i, j), None)
            if parent:
                self.win.draw_move(
                    self.cells[i][j], self.cells[parent[0]][parent[1]]
                )
            if i == self.num_rows - 1 and j == self.num_cols - 1:
                self._draw_path(parents)
                return True
            for k in range(4):
                ni, nj = i + DIRECTIONS[k], j + DIRECTIONS[k + 1]
                # continue if a wall is in the way
                if self._blocked(i, j, k):
                    continue
                if self._is_unvisited(ni, nj):
                    parents[(ni, nj)] = (i, j)
                    stack.append((ni, nj))

        return False

    def _solve_bfs(self):
        queue = deque([(0, 0)])
        parents = defaultdict(tuple)

        while queue:
            self._animate()
            i, j = queue.popleft()
            self.cells[i][j]
            self.cells[i][j].visited = True
            self._draw_cell(i, j)
            parent = parents.get((i, j), None)
            if parent:
                self.win.draw_move(
                    self.cells[i][j], self.cells[parent[0]][parent[1]]
                )
            if i == self.num_rows - 1 and j == self.num_cols - 1:
                self._draw_path(parents)
                return True
            for k in range(4):
                ni, nj = i + DIRECTIONS[k], j + DIRECTIONS[k + 1]
                # continue if a wall is in the way
                if self._blocked(i, j, k):
                    continue
                if self._is_unvisited(ni, nj):
                    parents[(ni, nj)] = (i, j)
                    queue.append((ni, nj))

        return False

    def _euclidian_distance_heuristic(
        self, i: int, j: int, dist: int
    ) -> float:
        return dist + sqrt((i - self.num_cols) ** 2 + (j - self.num_rows) ** 2)

    def _solve_a_star(self) -> bool:
        # shorten the function name for the euclidian distance heuristic
        # NOTE: can probably hot-swap heuristics using a parameter later
        f = self._euclidian_distance_heuristic
        heap = [(f(0, 0, 0), 0, 0, 0)]
        parents = {}

        while heap:
            self._animate()
            _, i, j, dist = heapq.heappop(heap)
            self.cells[i][j].visited = True
            self._draw_cell(i, j)
            parent = parents.get((i, j), None)
            if parent:
                self.win.draw_move(
                    self.cells[i][j], self.cells[parent[0]][parent[1]]
                )
            if i == self.num_cols - 1 and j == self.num_rows - 1:
                self._draw_path(parents)
                return True
            for k in range(4):
                ni, nj = i + DIRECTIONS[k], j + DIRECTIONS[k + 1]
                # continue if a wall is in the way
                if self._blocked(i, j, k):
                    continue
                if self._is_unvisited(ni, nj):
                    parents[(ni, nj)] = (i, j)
                    heapq.heappush(heap, (f(ni, nj, dist + 1), ni, nj, dist))

        return False

    def _blocked(self, i, j, k) -> bool:
        if k == DOWN and self.cells[i][j].has_bottom:
            return True
        elif k == RIGHT and self.cells[i][j].has_right:
            return True
        elif k == UP and self.cells[i][j].has_top:
            return True
        elif k == LEFT and self.cells[i][j].has_left:
            return True
        return False

    def _draw_path(self, parents: Dict[tuple, tuple]):
        prev = (self.num_cols - 1, self.num_rows - 1)
        curr = parents[prev]
        while True:
            self._animate()
            self.win.draw_move(
                self.cells[prev[0]][prev[1]],
                self.cells[curr[0]][curr[1]],
                True,
            )
            if curr == (0, 0):
                break
            tmp = prev
            prev = curr
            curr = parents[tmp]

    def _is_unvisited(self, i: int, j: int) -> bool:
        return (
            0 <= i < self.num_cols
            and 0 <= j < self.num_rows
            and not self.cells[i][j].visited
        )
