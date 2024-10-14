from tkinter import Canvas
from .point import Point
from .line import Line


class Cell:
    def __init__(
        self, origin: Point, width: int, height: int, thickness: int = 2
    ):
        self.origin = origin
        self.width = width
        self.height = height
        self.has_top = True
        self.has_right = True
        self.has_bottom = True
        self.has_left = True
        self.thickness = thickness
        self._create_lines()
        self.visited = False

    def _create_lines(self):
        x1, y1 = self.origin.x, self.origin.y
        x2, y2 = x1 + self.width, y1 + self.height
        offset = self.thickness / 2
        self.top = Line(
            Point(x1, y1 + offset), Point(x2, y1 + offset), self.thickness
        )
        self.bottom = Line(
            Point(x1, y2 - offset), Point(x2, y2 - offset), self.thickness
        )
        self.left = Line(
            Point(x1 + offset, y1), Point(x1 + offset, y2), self.thickness
        )
        self.right = Line(
            Point(x2 - offset, y1), Point(x2 - offset, y2), self.thickness
        )

    def draw(self, canvas: Canvas, color: str):
        if self.visited:
            canvas.create_rectangle(
                self.origin.x,
                self.origin.y,
                self.origin.x + self.width,
                self.origin.y + self.height,
                fill="#dddddd",
                width=0,
            )
        if self.has_top:
            self.top.draw(canvas, color)
        if self.has_right:
            self.right.draw(canvas, color)
        if self.has_bottom:
            self.bottom.draw(canvas, color)
        if self.has_left:
            self.left.draw(canvas, color)
