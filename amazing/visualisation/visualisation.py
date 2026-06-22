from amazing.maze_generator.a_maze_ing import MazeGrid
from termcolor import colored, cprint
import sys

def prRed(s): print("\033[91m {}\033[00m".format(s))
def prGreen(s): print("\033[92m\033[1m {}\033[00m".format(s), end= " ")
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


class Visualisation:
    __c_w: int
    __c_h: int
    __m_w: int
    __m_h: int

    def __init__(self, c_h: int, c_w: int, m_h: int, m_w):
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = m_h
        self.__m_w = m_w

    def pixel(self, ph: int):
        print(f"{\033[92mu'\u256c'}", end="")

        # for x in test:
        #     for i in range(10):
        #         print(f"{u'\u256c'}", end="")
        #     print(f"{ascii(x)}", end="")
        #     print()
        


def visualisation_maze(maze: MazeGrid) -> None:
    visu: Visualisation = Visualisation(4,4,5,5)
    visu.pixel(100)
