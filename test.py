import unittest

from maze import Maze
from primitives import Cell, Point


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 20
        num_cols = 10
        width = 10
        height = 12
        m = Maze(num_cols, num_rows, width, height, 0, None)
        self.assertEqual(len(m.cells), num_cols)
        self.assertEqual(len(m.cells[0]), num_rows)
        for row in range(num_rows):
            for col in range(num_cols):
                cell = m.cells[col][row]
                self.assertEqual(cell.origin.x, col * width)
                self.assertEqual(cell.origin.y, row * height)

    def test_maze_break_entrance_and_exit(self):
        m1 = Maze(20, 20, 10, 10, 0, None)
        self.assertFalse(m1.cells[0][0].has_top)
        self.assertFalse(m1.cells[-1][-1].has_bottom)

    def test_maze_break_directions(self):
        m1 = Maze(3, 3, 10, 10, 10, None)
        m1._break_down(1, 1)
        self.assertFalse(m1.cells[1][1].has_bottom or m1.cells[1][2].has_top)
        m1._break_right(1, 1)
        self.assertFalse(m1.cells[1][1].has_right or m1.cells[2][1].has_left)
        m1._break_up(1, 1)
        self.assertFalse(m1.cells[1][1].has_top, m1.cells[1][0].has_bottom)
        m1._break_left(1, 1)
        self.assertFalse(m1.cells[1][1].has_left, m1.cells[0][1].has_right)

    def test_cell_attributes(self):
        origin = Point(10, 20)
        width = 11
        height = 12
        thickness = 4
        cell = Cell(origin, width, height, thickness)
        # check that the cell is, in fact, a square
        self.assertEqual(cell.top.start.y, cell.top.end.y)
        self.assertEqual(cell.right.start.x, cell.right.end.x)
        self.assertEqual(cell.bottom.start.y, cell.bottom.end.y)
        self.assertEqual(cell.left.start.x, cell.left.end.x)
        self.assertEqual(cell.top.start.x, cell.bottom.start.x)
        self.assertEqual(cell.top.end.x, cell.bottom.end.x)
        self.assertEqual(cell.left.start.y, cell.right.start.y)
        self.assertEqual(cell.left.end.y, cell.right.end.y)
        # check each unique x and y value in the square
        self.assertEqual(origin.x, cell.top.start.x)
        self.assertEqual(origin.x + width, cell.top.end.x)
        self.assertEqual(origin.y, cell.left.start.y)
        self.assertEqual(origin.y + height, cell.left.end.y)
        self.assertEqual(origin.x + thickness / 2, cell.left.start.x)
        self.assertEqual(origin.x + width - thickness / 2, cell.right.start.x)
        self.assertEqual(origin.y + thickness / 2, cell.top.start.y)
        self.assertEqual(
            origin.y + height - thickness / 2, cell.bottom.start.y
        )
