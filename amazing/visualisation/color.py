from typing import Literal

class Color:
    def RED(str) -> str: return print(f"\033[91m{str}\033[00m".format(str))
    def GREEN(str) -> str: return print(f"\033[92m{str}\033[00m".format(str))