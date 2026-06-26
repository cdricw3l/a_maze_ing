from amazing.maze_generator.maze import MazeGrid, get_maze
from amazing.visualisation import visualisation_maze
from amazing.visualisation.color import Color
import signal
import sys


def color_choice() -> str:
    print("color (white by default): Red:1 Green:2 Yellow:3 LightPurple:4 Purple:5 Cyan:6 LightGray:7 Black:8")
    input_user: str = input("")
    match input_user:
        case "1":
            return "\033[91m"
        case "2":
            return "\033[92m"
        case "3":
            return "\033[93m"
        case "4":
            return "\033[94m"
        case "5":
            return "\033[95m"
        case "6":
            return "\033[96m"
        case "7":
            return "\033[97m"
        case "8":
            return "\033[90m"
        case _:
            print("color by default: white")
    return  "\033[0m"

def maze_menu(config_file: str) -> int:
    maze : MazeGrid = get_maze(config_file)
    visualisation_maze(maze, "\033[0m")
    try:
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Rotate maze colors")
            print("5. Quit")
            user_input = input("Choice? (1-5): ")
            match user_input:
                case "1":
                    maze : MazeGrid = get_maze(config_file)
                    visualisation_maze(maze, "\033[0m")
                case "2":
                    maze : MazeGrid = get_maze(config_file)
                    visualisation_maze(maze, "\033[0m")
                case "3":
                    maze : MazeGrid = get_maze(config_file)
                    color: str = color_choice()
                    visualisation_maze(maze, color)
                case "4":
                    forty_two_color: str = color_choice()
                    visualisation_maze(maze, color, forty_two_color)
                    return 0
                case "5":
                    return 0
                case _:
                    print("Choose a valide input between 1-4 or quit with 5")
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

    