from maze import Maze
from window import Window


if __name__ == "__main__":
    width, height = 800, 500
    cell_width, cell_height = 50, 50
    window = Window(width, height)
    maze = Maze(width // cell_width, height // cell_height, cell_width, cell_height, window)
    window.redraw()
    maze.draw()
    maze.solve()
    window.wait_for_close()