import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_rows = 20
        num_cols = 10
        width = 10
        height = 12
        m = Maze(num_rows, num_cols, width, height, None)
        self.assertEqual(len(m.cells), num_rows)
        self.assertEqual(len(m.cells[0]), num_cols)
        for row in range(num_rows):
            for col in range(num_cols):
                cell = m.cells[row][col]
                self.assertEqual(cell.origin.x, col * width)
                self.assertEqual(cell.origin.y, row * height)
                # check top line
                self.assertEqual(cell.top.start.x, cell.origin.x)
                self.assertEqual(cell.top.start.y, cell.origin.y + cell.thickness/2)
                self.assertEqual(cell.top.end.x, cell.origin.x + width)
                self.assertEqual(cell.top.end.y, cell.origin.y + cell.thickness/2)
                # check bottom line
                self.assertEqual(cell.bottom.start.y, cell.origin.y + height - cell.thickness/2)
                self.assertEqual(cell.bottom.start.x, cell.origin.x)
                self.assertEqual(cell.bottom.end.y, cell.origin.y + height - cell.thickness/2)
                self.assertEqual(cell.bottom.end.x, cell.origin.x + width)
                # check left line
                self.assertEqual(cell.left.start.x, cell.origin.x + cell.thickness/2)
                self.assertEqual(cell.left.start.y, cell.origin.y)
                self.assertEqual(cell.left.end.x, cell.origin.x + cell.thickness/2)
                self.assertEqual(cell.left.end.y, cell.origin.y + height)
                # check right line
                self.assertEqual(cell.right.start.x, cell.origin.x + width - cell.thickness/2)
                self.assertEqual(cell.right.start.y, cell.origin.y)
                self.assertEqual(cell.left.end.x, cell.origin.x + cell.thickness/2)
                self.assertEqual(cell.left.end.y, cell.origin.y + height)

    def test_maze_break_entrance_and_exit(self):
        m1 = Maze(20, 20, 10, 10, None)
        self.assertFalse(m1.cells[0][0].has_top)
        self.assertFalse(m1.cells[-1][-1].has_bottom)