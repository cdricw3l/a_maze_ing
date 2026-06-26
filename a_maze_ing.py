from amazing.maze_generator.maze import MazeGrid, get_maze
from amazing.visualisation import visualisation_maze
from amazing.visualisation.color import Color
import signal
import sys

def maze_menu(config_file: str) -> int:
    maze : MazeGrid = get_maze(config_file)
    visualisation_maze(maze)

    try:
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            user_input = input("Choice? (1-4): ")
            match user_input:
                case "1":
                    maze : MazeGrid = get_maze(config_file)
                    visualisation_maze(maze)
                case "4":
                    return 0
                case _:
                    print("Choose a valide input between 1-3 or quit with 4")
                    continue
    except (Exception, KeyboardInterrupt):
        return 0

if __name__ == "__main__":
    arg: list[str] = sys.argv[1:]
    if len(arg) != 1:
        Color.RED("Configuration path is missing")
    else:
        maze_menu(arg[0])
        print("End of the programme")

    