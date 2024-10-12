from tkinter import Canvas

from .point import Point


class Line:
    def __init__(self, start: Point, end: Point, width: int = 2):
        self.start = start
        self.end = end
        self.width = width

    def draw(self, canvas: Canvas, color: str):
        canvas.create_line(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            fill=color,
            width=self.width,
        )
