from visualisation.color import Color_bg, Color_line
from mazegen.mazegen import MazeGrid, get_maze
from visualisation.visualisation import visualisation_maze
import time


def color_line() -> str:
    print(f"=== 42 maze colors === (white by default)\n\
1:{Color_line.BLACK}Black{Color_line.RESET}\n\
2:{Color_line.RED}Red{Color_line.RESET}\n\
3:{Color_line.GREEN}Green{Color_line.RESET}\n\
4:{Color_line.YELLOW}Yellow{Color_line.RESET}\n\
5:{Color_line.BLUE}Blue{Color_line.RESET}\n\
6:{Color_line.PURPLE}Purple{Color_line.RESET}\n\
7:{Color_line.CYAN}Cyan{Color_line.RESET}\n\
8:{Color_line.WHITE}White{Color_line.RESET}")
    input_user: str = input("Choice? (1-9): ").strip()
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
            return Color_line.PURPLE
        case "7":
            return Color_line.CYAN
        case "8":
            return Color_line.WHITE
        case _:
            print("color by default: white")
            return Color_line.WHITE


def background_color(field: str) -> str:
    print(f"{field}\n\
1:{Color_bg.TRANSPARANT}Transparent {Color_bg.RESET}\n\
2:{Color_bg.BLACK}Black{Color_bg.RESET}\n\
3:{Color_bg.RED}Red{Color_bg.RESET}\n\
4:{Color_bg.GREEN}Green{Color_bg.RESET}\n\
5:{Color_bg.YELLOW}Yellow{Color_bg.RESET}\n\
6:{Color_bg.BLUE}Blue{Color_bg.RESET}\n\
7:{Color_bg.PURPLE}Purple{Color_bg.RESET}\n\
8:{Color_bg.CYAN}Cyan{Color_bg.RESET}\n\
9:{Color_bg.WHITE}White{Color_bg.RESET}")
    input_user: str = input("Choice? (1-9): ").strip()
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
            return Color_bg.CYAN
        case "9":
            return Color_bg.WHITE
        case _:
            print("color by default: white")
            return Color_bg.WHITE


def maze_menu(config_file: str) -> int:
    maze: MazeGrid = get_maze(config_file)
    color_l: str = Color_line.CYAN
    color_bg: str = Color_bg.GREEN
    color_path: str = Color_bg.PURPLE
    path_state: bool = False
    state: bool = visualisation_maze(
        maze,
        color_l,
        color_bg,
        color_path,
        path_state)
    try:
        while state:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Rotate 42 colors")
            print("5. Rotate Path colors")
            print("6. Quit")
            user_input = input("Choice? (1-5): ").strip()
            match user_input:
                case "1":
                    maze = get_maze(config_file)
                    state = visualisation_maze(
                        maze,
                        color_l,
                        color_bg,
                        color_path,
                        path_state)
                case "2":
                    if path_state is False:
                        path_state = True
                    else:
                        path_state = False
                    state = visualisation_maze(maze,
                                               color_l,
                                               color_bg,
                                               color_path, path_state)
                case "3":
                    color_l = color_line()
                    state = visualisation_maze(
                        maze,
                        color_l,
                        color_bg,
                        color_path,
                        path_state)
                case "4":
                    color_bg = background_color(
                        "=== 42 background colors === (white by default)")
                    state = visualisation_maze(maze,
                                               color_l,
                                               color_bg,
                                               color_path,
                                               path_state)
                case "5":
                    color_path = background_color(
                        "=== 42 shortest path colors === (green by default)")
                    state = visualisation_maze(maze,
                                               color_l,
                                               color_bg,
                                               color_path,
                                               path_state)
                case "6":
                    return 0
                case _:
                    print(f"{Color_line.RED}"
                          f"Choose a valide input between 1-4 "
                          f"or quit with 5{Color_line.RESET}")
                    time.sleep(0.5)
                    continue
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        return 0
    return 1
