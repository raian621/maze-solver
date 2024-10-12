from collections import defaultdict
from random import randint
from time import sleep

from primitives import Cell, Point
from window import Window


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
        win(int): The `Window` object
        cells(List[List[Cell]]): The matrix of cells that make up the maze
    """
    def __init__(
        self,
        num_cols: int,
        num_rows: int,
        cell_width: int,
        cell_height: int,
        win: Window,
    ):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls()
        self.clear_cell_states()

    def clear_cell_states(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def _create_cells(self):
        self.cells = [[None] * self.num_cols for _ in range(self.num_rows)]
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.cells[row][col] = Cell(
                    Point(col * self.cell_width, row * self.cell_height),
                    self.cell_width,
                    self.cell_height,
                )

    def _draw_cell(self, row: int, col: int):
        self.win.draw_cell(self.cells[row][col])

    def _animate(self):
        self.win.redraw()
        sleep(0.005)

    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top = False
        self.cells[-1][-1].has_bottom = False

    def _break_walls(self):
        stack = [(0, 0)]
        dirs = [0, 1, 0, -1, 0]  # right, down, left, up

        while stack:
            i, j = stack.pop()
            self.cells[i][j].visited = True
            choices = []
            for k in range(4):
                ni, nj = i + dirs[k], j + dirs[k + 1]
                if (
                    0 <= ni < self.num_rows
                    and 0 <= nj < self.num_cols
                    and not self.cells[ni][nj].visited
                ):
                    choices.append(k)
                    stack.append((ni, nj))

            # break a random wall if there's an unvisited cell adjacent to the
            # current cell
            if len(choices) > 0:
                r = randint(0, len(choices) - 1)
                k = choices[r]
                ni, nj = i + dirs[k], j + dirs[k + 1]
                current = self.cells[ni][nj]
                neighbor = self.cells[i][j]
                if k == 0: # left
                    current.has_left = False
                    neighbor.has_right = False
                elif k == 1: # up
                    current.has_top = False
                    neighbor.has_bottom = False
                elif k == 2: # right
                    current.has_right = False
                    neighbor.has_left = False 
                else: # down
                    current.has_bottom = False
                    neighbor.has_top = False

    def draw(self):
        for row in range(self.num_rows):
          for col in range(self.num_cols):
              self._draw_cell(row, col)
    
    def solve(self, algorithm: str = "dfs") -> bool:
        if algorithm == "dfs":
            return self._solve_dfs()

    def _solve_dfs(self):
        stack = [(0, 0)]
        dirs = [0, 1, 0, -1, 0]
        parents = defaultdict(tuple)

        while stack:
            self._animate()
            i, j = stack.pop()
            self.cells[i][j].visited = True
            self._draw_cell(i, j)
            parent = parents.get((i, j), None)
            if parent:
                self.win.draw_move(self.cells[i][j], self.cells[parent[0]][parent[1]])
            if i == self.num_rows-1 and j == self.num_cols-1:
                # draw path:
                prev = (self.num_rows-1, self.num_cols-1)
                curr = parents[prev]
                while True:
                    self.win.draw_move(
                        self.cells[prev[0]][prev[1]],
                        self.cells[curr[0]][curr[1]],
                        True
                    )
                    if curr == (0, 0):
                        break
                    tmp = prev
                    prev = curr
                    curr = parents[tmp]
                return True
            for k in range(4):
                ni, nj = i + dirs[k], j + dirs[k+1]
                # continue if a wall is in the way
                if k == 0 and self.cells[i][j].has_right:
                    continue
                elif k == 1 and self.cells[i][j].has_bottom:
                    continue
                elif k == 2 and self.cells[i][j].has_left:
                    continue
                elif k == 3 and self.cells[i][j].has_top:
                    continue
                if (
                    0 <= ni < self.num_rows
                    and 0 <= nj < self.num_cols
                    and not self.cells[ni][nj].visited
                ):
                    parents[(ni, nj)] = (i, j)
                    stack.append((ni, nj))

        return False