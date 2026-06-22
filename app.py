from amazing.maze_generator import MazeGrid, get_maze
from amazing.visualisation import visualisation_maze



if __name__ == "__main__":
    maze : MazeGrid = get_maze("config/config.txt")
    visualisation_maze(maze)
    