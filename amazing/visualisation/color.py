from enum import Enum

class Color_bg():
    TRANSPARANT: str = "\033[48m"
    BLACK: str = "\033[40m"
    RED: str = "\033[41m"
    GREEN: str = "\033[42m"
    YELLOW: str = "\033[43m"
    BLUE: str = "\033[44m"
    PURPLE: str = "\033[45m"
    CYAN: str = "\033[46m"
    WHITE: str = "\033[47m"
    DEFAULT: str = "\033[47m"
    RESET: str = "\033[0m"

class Color_line():
    BLACK: str = "\033[90m"
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    BLUE: str = "\033[94m"
    PURPLE: str = "\033[95m"
    CYAN: str = "\033[96m"
    WHITE: str = "\033[97m"
    DEFAULT: str = "\033[97m"
    RESET: str = "\033[0m"