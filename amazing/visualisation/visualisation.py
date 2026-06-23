from amazing.maze_generator.maze import MazeGrid, Cell
import sys
from collections import defaultdict
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

    @staticmethod
    def first_line(cell: int, inter_cel: int) -> str:
        line: str = ""

        for i in range(cell):
            x: int = 0
            if i == 0:
                line += Char.LT
            elif i == cell - 1:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                line += Char.RT
            else:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                if i < cell - 1:
                    line = line + Char.JT
        return line
    
    @staticmethod
    def last_line(cell: int, inter_cel: int) -> str:
        line: str = ""

        for i in range(cell):
            x: int = 0
            if i == 0:
                line += Char.LB
            elif i == cell - 1:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                line += Char.RB

            else:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                if i < cell - 1:
                    line = line + Char.JB
        return line
    
    @staticmethod
    def midle_line(cell: int, inter_cel: int) -> str:
        line: str = ""

        for i in range(cell):
            x: int = 0
            if i == 0:
                line += Char.V
            elif i == cell - 1:
                while x < inter_cel:
                    line = line + " "
                    x+=1
                line += Char.V
            else:
                while x < inter_cel:
                    line = line + " "
                    x+=1
                if i < cell - 1:
                    line = line + Char.V
        return line
    
    @staticmethod
    def jonction_line(cell: int, inter_cel: int) -> str:
        line: str = ""

        for i in range(cell):
            x: int = 0
            if i == 0:
                line += Char.JL
            elif i == cell - 1:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                line += Char.JR
            else:
                while x < inter_cel:
                    line = line + Char.H
                    x+=1
                if i < cell - 1:
                    line = line + Char.JM
        return line

    def visu(self, cells: list[tuple[str, ...]], nb_cell: int) -> None:


        for i in range(nb_cell):
            if i == 0:
                print(f"\033[92m{self.first_line(nb_cell , 10)}")
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.jonction_line(nb_cell , 10))
            elif i == nb_cell - 1:
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.last_line(nb_cell, 10))
            elif i < nb_cell - 2:
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.midle_line(nb_cell , 10))
                print(self.jonction_line(nb_cell , 10))



def get_bits(cell: tuple[float, ...], open_neighbors: list[Cell]) -> int :


    nord: tuple[float, ...] = (cell[0] - 1 , cell[1]) 
    est: tuple[float, ...] = (cell[0] , cell[1] + 1) 
    sud: tuple[float, ...] = (cell[0] + 1 , cell[1])
    west: tuple[float, ...] = (cell[0] , cell[1] - 1)

    # the binary value of 0 is 0000
    value: int = 0

    #this mask active the first bit for the West wall
    # if the West variable tuple is on neighbour list this bit is activate
    # print(f"nord: {nord}")
    # print(f"est: {est}")
    # print(f"sud: {sud}")
    # print(f"west: {west}")
    # print(f"neghbour {open_neighbors}")
    if west in open_neighbors:
        print("acive 1")
        value = value | (1 << 0)
    #this mask active the second bit for the South wall
    # if the South variable tuple is on neighbour list this bit is activate
    if sud in open_neighbors:
        print("acive 2")
        value = value | (1 << 1)
    #this mask active the third bit for the Est wall
    # if the Est variable tuple is on neighbour list this bit is activate
    if est in open_neighbors:
        print("acive 3")
        value = value | (1 << 2)
    #this mask active the fourth bit for the Nord wall
    # if the Nord variable tuple is on neighbour list this bit is activate
    if nord in open_neighbors:
        print("acive 4")
        value = value | (1 << 3)

    return value
     

def get_output(maze: MazeGrid) -> dict[tuple[float,...]: int]:
    
    """ 
    return a dict with cell coordonee as key and 
    integer value who represente which wall is open 
    exemple 0100 -> only east wall is open
    """

    graph: defaultdict[Cell, list[Cell]] = maze.graph
    output: dict[tuple[float, ...]: int] = {}
    for cell in graph:
        open_neighbors: list[Cell] = graph.get(cell)
        key: tuple[float, ...] = cell
        value: int = get_bits(key, open_neighbors)
        output.update({key:value})
    
    return output

def visualisation_maze(maze: MazeGrid) -> None:
    print(f"width {maze.width}")
    print(f"height {maze.height}")
    print(f"height {maze.height * maze.width}\n")

    output: dict[tuple[float, ...]: int] = get_output(maze)
    for o in output:
        print(f"cell: {o}, wall: {output.get(o), format(output.get(o), 'b')}, neighbour: {maze.graph.get(o)}")

    