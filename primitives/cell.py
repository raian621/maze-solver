from tkinter import Canvas
from .point import Point
from .line import Line


class Cell:
    def __init__(self, origin: Point, width: int, height: int, thickness: int = 2):
        self.origin = origin
        self.width = width
        self.height = height
        self.has_top = True
        self.has_right = True
        self.has_bottom = True
        self.has_left = True
        self.thickness = thickness
        self.top = Line(
            Point(self.origin.x, self.origin.y + thickness / 2),
            Point(self.origin.x + width, self.origin.y + thickness / 2),
            thickness
        )
        self.right = Line(
            Point(self.origin.x + width - thickness / 2, self.origin.y),
            Point(self.origin.x + width - thickness / 2, self.origin.y + height),
            thickness
        )
        self.bottom = Line(
            Point(self.origin.x, self.origin.y + height - thickness/2),
            Point(self.origin.x + width, self.origin.y + height - thickness/2),
            thickness,
        )
        self.left = Line(
            Point(self.origin.x + thickness / 2, self.origin.y),
            Point(self.origin.x + thickness / 2, self.origin.y + height),
            thickness,
        )
        self.visited = False

    def draw(self, canvas: Canvas, color: str):
        if self.visited:
            canvas.create_rectangle(
                self.origin.x,
                self.origin.y,
                self.origin.x + self.width,
                self.origin.y + self.height,
                fill="#dddddd",
                width=0 
            )
        if self.has_top:
            self.top.draw(canvas, "red")
        if self.has_right:
            self.right.draw(canvas, "green")
        if self.has_bottom:
            self.bottom.draw(canvas, "blue")
        if self.has_left:
            self.left.draw(canvas, color)
