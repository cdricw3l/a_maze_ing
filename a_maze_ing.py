from amazing.maze_generator.maze import MazeGrid, get_maze
from amazing.visualisation import visualisation_maze
from amazing.visualisation.color import Color
import sys



if __name__ == "__main__":
    arg: list[str] = sys.argv[1:]
    if len(arg) != 1:
        Color.RED("Configuration path is missing")
    else:
        maze : MazeGrid = get_maze(arg[0])
        visualisation_maze(maze)
    