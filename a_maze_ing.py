
from menu.menu import maze_menu, Color_line
import sys

if __name__ == "__main__":
    arg: list[str] = sys.argv[1:]

    if len(arg) != 1:
        print(
            f"{Color_line.RED}"
            "Configuration path is missing"
            f"{Color_line.RESET}"
        )
    else:
        maze_menu(arg[0])
        print("End of the programme")
