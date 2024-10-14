from tkinter import Canvas, Tk

from primitives import Cell, Point, Line


class Window:
    def __init__(self, width: int, height: int, title: str = "Maze Solver"):
        self.__root = Tk()
        self.__root.title(title)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.width = width
        self.height = height
        self.canvas = Canvas(
            width=width,
            height=height,
        )
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line):
        line.draw(self.canvas, "black")

    def draw_cell(self, cell: Cell):
        cell.draw(self.canvas, "black")

    def draw_move(self, from_cell: Cell, to_cell: Cell, undo=False):
        line = Line(
            Point(
                from_cell.origin.x + from_cell.width // 2,
                from_cell.origin.y + from_cell.height // 2,
            ),
            Point(
                to_cell.origin.x + to_cell.width // 2,
                to_cell.origin.y + to_cell.height // 2,
            ),
        )
        line.draw(self.canvas, "magenta" if undo else "gray")
