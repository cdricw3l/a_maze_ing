from amazing.maze_generator.a_maze_ing import MazeGrid
from termcolor import colored, cprint
import sys
import typing

def prRed(s): print("\033[91m {}\033[00m".format(s))
def prGreen(s): print("\033[92m {}\033[00m".format(s), end= " ")
def prYellow(s): print("\033[93m {}\033[00m".format(s))
def prLightPurple(s): print("\033[94m {}\033[00m".format(s))
def prPurple(s): print("\033[95m {}\033[00m".format(s))
def prCyan(s): print("\033[96m {}\033[00m".format(s))
def prLightGray(s): print("\033[97m {}\033[00m".format(s))
def prBlack(s): print("\033[90m {}\033[00m".format(s))


test = [u'\u2502',   #  0x00b3 -> BOX DRAWINGS LIGHT VERTICAL
        u'\u2524',   #  0x00b4 -> BOX DRAWINGS LIGHT VERTICAL AND LEFT
        u'\u2561',   #  0x00b5 -> BOX DRAWINGS VERTICAL SINGLE AND LEFT DOUBLE
        u'\u2562',   #  0x00b6 -> BOX DRAWINGS VERTICAL DOUBLE AND LEFT SINGLE
        u'\u2556',   #  0x00b7 -> BOX DRAWINGS DOWN DOUBLE AND LEFT SINGLE
        u'\u2555',   #  0x00b8 -> BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE
        u'\u2551',   #  0x00ba -> BOX DRAWINGS DOUBLE VERTICAL
        u'\u2557',   #  0x00bb -> BOX DRAWINGS DOUBLE DOWN AND LEFT
        u'\u255d',   #  0x00bc -> BOX DRAWINGS DOUBLE UP AND LEFT
        u'\u255c',   #  0x00bd -> BOX DRAWINGS UP DOUBLE AND LEFT SINGLE
        u'\u255b',   #  0x00be -> BOX DRAWINGS UP SINGLE AND LEFT DOUBLE
        u'\u2510',   #  0x00bf -> BOX DRAWINGS LIGHT DOWN AND LEFT
        u'\u2514',   #  0x00c0 -> BOX DRAWINGS LIGHT UP AND RIGHT
        u'\u2534',   #  0x00c1 -> BOX DRAWINGS LIGHT UP AND HORIZONTAL
        u'\u252c',   #  0x00c2 -> BOX DRAWINGS LIGHT DOWN AND HORIZONTAL
        u'\u251c',   #  0x00c3 -> BOX DRAWINGS LIGHT VERTICAL AND RIGHT
        u'\u2500',   #  0x00c4 -> BOX DRAWINGS LIGHT HORIZONTAL
        u'\u253c',   #  0x00c5 -> BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL
        u'\u255e',   #  0x00c6 -> BOX DRAWINGS VERTICAL SINGLE AND RIGHT DOUBLE
        u'\u255f',   #  0x00c7 -> BOX DRAWINGS VERTICAL DOUBLE AND RIGHT SINGLE
        u'\u255a',   #  0x00c8 -> BOX DRAWINGS DOUBLE UP AND RIGHT
        u'\u2554',   #  0x00c9 -> BOX DRAWINGS DOUBLE DOWN AND RIGHT
        u'\u2569',   #  0x00ca -> BOX DRAWINGS DOUBLE UP AND HORIZONTAL
        u'\u2566',   #  0x00cb -> BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
        u'\u2560',   #  0x00cc -> BOX DRAWINGS DOUBLE VERTICAL AND RIGHT ----------------------> right vetical wall
        u'\u2563',   #  0x00b9 -> BOX DRAWINGS DOUBLE VERTICAL AND LEFT -----------------------------> left vertical wall

        u'\u2550',   #  0x00cd -> BOX DRAWINGS DOUBLE HORIZONTAL
        u'\u256c',   #  0x00ce -> BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
        u'\u2567',   #  0x00cf -> BOX DRAWINGS UP SINGLE AND HORIZONTAL DOUBLE
        u'\u2568',   #  0x00d0 -> BOX DRAWINGS UP DOUBLE AND HORIZONTAL SINGLE ---------------------------> top line
        u'\u2564',   #  0x00d1 -> BOX DRAWINGS DOWN SINGLE AND HORIZONTAL DOUBLE -------------------------> inside wall line
        u'\u2565',   #  0x00d2 -> BOX DRAWINGS DOWN DOUBLE AND HORIZONTAL SINGLE -------------------------> bottom line
        u'\u2559',   #  0x00d3 -> BOX DRAWINGS UP DOUBLE AND RIGHT SINGLE
        u'\u2558',   #  0x00d4 -> BOX DRAWINGS UP SINGLE AND RIGHT DOUBLE
        u'\u2552',   #  0x00d5 -> BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE
        u'\u2553',   #  0x00d6 -> BOX DRAWINGS DOWN DOUBLE AND RIGHT SINGLE
        u'\u256b',   #  0x00d7 -> BOX DRAWINGS VERTICAL DOUBLE AND HORIZONTAL SINGLE
        u'\u256a',   #  0x00d8 -> BOX DRAWINGS VERTICAL SINGLE AND HORIZONTAL DOUBLE
        u'\u2518',   #  0x00d9 -> BOX DRAWINGS LIGHT UP AND LEFT
        u'\u250c' ]  #  0x00da -> BOX DRAWINGS LIGHT DOWN AND RIGHT


class Char:
    LT: typing.Literal[True] = '╔'
    LB: typing.Literal[True] = '╚' 
    RT: typing.Literal[True] = '╗' 
    RB: typing.Literal[True] = '╝' 
    JT: typing.Literal[True] = '╦'
    JB: typing.Literal[True] = '╩'
    JL: typing.Literal[True] = '╠'
    JR: typing.Literal[True] = '╣'
    JM: typing.Literal[True] = '╬'
    H: typing.Literal[True] = '═'
    V: typing.Literal[True] = '║'

class Drawing:


    def __init__(self):
        self.__char = {"DOUBLE_VERTI_PIPE" : u'\u2551', "DOUBLE_RIGHT_TOP" : u'\u2557', "DOUBLE_LEFT_TOP" : u'\u2554',
                       "DOUBLE_LEFT_BOTTOM" : u'\u255a', "DOUBLE_RIGHT_BOTTOM" :u'\u255d', "DOUBLE_HORIZ_PIPE" : u'\u2550', "joint": u'\u2566'}
    
    def line(self, size: int, c: str):
        for i in range(size):
            print(c, end="", flush=True)


class Visualisation:
    __c_w: float
    __c_h: float
    __m_h: float
    __m_w: float


    def __init__(self, c_h: float, c_w: float, m_h: float, m_w: float):
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = m_h
        self.__m_w = m_w

    def test(self):
        symbs = [u'\u255a', u'\u2554', u'\u2569', u'\u2566', u'\u2560', u'\u2550', u'\u256c']
        for sym in symbs:
            print(sym)
            print()

    def visu(self, cells: list[tuple[str, ...]]) -> None:
        # symbs = [u'\u255a', u'\u2554', u'\u2569', u'\u2566', u'\u2560', u'\u2550', u'\u256c']
        # for sym in symbs:
        #     print(sym)
        char: Char = Char()
        draw: Drawing = Drawing()
        for x in range(self.__m_h * self.__c_h):
            p = 0
            for y in range(self.__m_w * self.__c_w):

                if x == 0 and y == 0 and p != 3:
                    draw.line(1,char.LT)
                elif x == 0 and y == (self.__c_w * self.__m_w - 1):
                    draw.line(1, char.RT)
                elif x == 0 and y == (self.__c_w * self.__m_w - 1) and p != 3:
                    draw.line(1, char.RT)
                elif x > 0 and y == 0 or x > 0 and p == 4:
                    draw.line(1, char.V)
                elif x == 0 and  p == 4:
                    draw.line(1, char.JT)
                    p = 0
                else:
                    draw.line(1, char.H)
                p += 1
            print()




def visualisation_maze(maze: MazeGrid) -> None:
    print(f"width {maze.width}")
    print(f"height {maze.height}")
    print(f"height {maze.height * maze.width}")

    i: int = 0
    visu: Visualisation = Visualisation(4,4, 5, 5)
    cells: list[tuple[str, ...]] = list(maze.graph.keys())[i: i + maze.width]
    #print(cells)
    visu.visu(cells)
    
    # for x in range(maze.height):
    #     cells: list[tuple[str, ...]] = list(maze.graph.keys())[i: i + maze.width]
    #     #print(cells)
    #     visu.visu(cells)
    #     i += 8
