from amazing.maze_generator.maze import MazeGrid, get_maze
from amazing.visualisation import visualisation_maze
from amazing.visualisation.color import Color_bg, Color_line
import signal
import sys


def color_line() -> str:
    print(f"=== 42 maze colors === (white by default)\n\
1:{Color_line.BLACK}Black{Color_bg.RESET}\n\
2:{Color_line.RED}Red{Color_bg.RESET}\n\
3:{Color_line.GREEN}Green{Color_bg.RESET}\n\
4:{Color_line.YELLOW}Yellow{Color_bg.RESET}\n\
5:{Color_line.BLUE}Blue{Color_bg.RESET}\n\
6:{Color_line.PURPLE}Purple{Color_bg.RESET}\n\
7:{Color_line.CYAN}Cyan{Color_bg.RESET}\n\
8:{Color_line.WHITE}White{Color_bg.RESET}")
    input_user: str = input("Choice? (1-9): ")
    match input_user:
        case "1":
            return Color_line.BLACK
        case "2":
            return Color_line.RED
        case "3":
            return Color_line.GREEN
        case "4":
            return Color_line.YELLOW
        case "5":
            return Color_line.BLUE
        case "6":
            return Color_bg.PURPLE
        case "7":
            return Color_line.PURPLE
        case "8":
            return Color_line.WHITE
        case _:
            print("color by default: white")
            return Color_bg.WHITE

def forty_two_colors() -> str:
    print(f"=== 42 background colors === (white by default)\n\
1:{Color_bg.TRANSPARANT}Transparent {Color_bg.RESET}\n\
2:{Color_bg.BLACK}Black{Color_bg.RESET}\n\
3:{Color_bg.RED}Red{Color_bg.RESET}\n\
4:{Color_bg.GREEN}Green{Color_bg.RESET}\n\
5:{Color_bg.YELLOW}Yellow{Color_bg.RESET}\n\
6:{Color_bg.BLUE}Blue{Color_bg.RESET}\n\
7:{Color_bg.PURPLE}Purple{Color_bg.RESET}\n\
8:{Color_bg.CYAN}Cyan{Color_bg.RESET}\n\
9:{Color_bg.WHITE}White{Color_bg.RESET}")
    input_user: str = input("Choice? (1-9): ")
    match input_user:
        case "1":
            return Color_bg.TRANSPARANT
        case "2":
            return Color_bg.BLACK
        case "3":
            return Color_bg.RED
        case "4":
            return Color_bg.GREEN
        case "5":
            return Color_bg.YELLOW
        case "6":
            return Color_bg.BLUE
        case "7":
            return Color_bg.PURPLE
        case "8":
            return Color_bg.PURPLE
        case "9":
            return Color_bg.WHITE
        case _:
            print("color by default: white")
            return Color_bg.WHITE

def maze_menu(config_file: str) -> int:
    maze : MazeGrid = get_maze(config_file)
    visualisation_maze(maze, Color_line.DEFAULT, Color_bg.DEFAULT)
    try:
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Rotate 42 colors")
            print("5. Quit")
            user_input = input("Choice? (1-5): ")
            match user_input:
                case "1":
                    maze : MazeGrid = get_maze(config_file)
                    visualisation_maze(maze, Color_line.DEFAULT, Color_bg.DEFAULT)
                case "2":
                    visualisation_maze(maze, Color_line.DEFAULT, Color_bg.DEFAULT)
                case "3":
                    color: str = color_line()
                    visualisation_maze(maze, color, Color_bg.DEFAULT)
                case "4":
                    forty_two_color: str = forty_two_colors()
                    visualisation_maze(maze, Color_line.DEFAULT, forty_two_color)
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
        Color_line.RED("Configuration path is missing")
    else:
        maze_menu(arg[0])
        print("End of the programme")

    