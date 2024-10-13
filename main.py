from typing import Dict
from maze import Maze
from window import Window

from getopt import getopt
from sys import argv, exit

options = "W:H:c:a:d:h"
long_options = ["width=", "height=", "cell-width=", "algorithm=", "delay=", "help"]


SUPPORTED_ALGORITHMS = set([
    "dfs", "bfs", "astar"
])
ALGORITHM_FULL_NAMES = {
    "dfs": "Depth-First Search",
    "bfs": "Breadth-First Search",
    "astar": "A-Star Search",
}
HELP = """
Usage: python main.py -[WHcad] <value> -h

Options:
    -a | --algorithm:
        Sets the pathfinding algorithm used to solve the maze. Supported
        algorithms include:
            - dfs: Depth-first search
            - bfs: Breadth-first search
            - astar: A-Star search
    -c | --cell-width:
        Sets the width of the cells in the maze
    -d | --delay:
        Sets the delay between steps in the maze solver algorithm
    -h | --help:
        Display this help text
    -H | --height:
        Sets the height of the GUI window
    -W | --width:
        Sets the width of the GUI window
"""


def get_opts() -> Dict[str, any]:
    opts = {}
    optlist, _ = getopt(argv[1:], options, long_options)
    should_exit = False

    for flag, value in optlist:
        if flag == "-W" or flag == "--width":
            opts["width"] = int(value)
        elif flag == "-H" or flag == "--height":
            opts["height"] = int(value)
        elif flag == "-c" or flag == "--cell-width":
            opts["cell_width"] = int(value)
        elif flag == "-a" or flag == "--algorithm":
            if value not in SUPPORTED_ALGORITHMS:
                print(f"Algorithm `{value}` not supported")
                should_exit = True
            opts["algorithm"] = value
        elif flag == "-d" or flag == "--delay":
            opts["delay"] = float(value)
        elif flag == "-h" or flag == "--help":
            print(HELP)
            exit(0)
        else:
            print(f"unknown option provided {flag}")
    
    if should_exit:
        exit(1)

    return opts


if __name__ == "__main__":
    opts = get_opts()
    width, height = opts.get("width", 800), opts.get("height", 500)
    cell_width, cell_height = opts.get("cell_width", 20), opts.get("cell_width", 20)
    algorithm = opts.get("algorithm", "dfs")
    delay = opts.get("delay", 0.033) # a lil less than 30 fps
    title = f"Maze Solver ({ALGORITHM_FULL_NAMES[algorithm]})"
    window = Window(width, height, title)
    maze = Maze(
        width // cell_width,
        height // cell_height,
        cell_width,
        cell_height,
        delay,
        window
    )
    window.redraw()
    maze.draw()
    maze.solve(algorithm)
    window.wait_for_close()