from amazing.maze_generator.maze import MazeGrid, Cell
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


class Visualisation:
    __c_w: float
    __c_h: float
    __m_h: float
    __m_w: float


    def __init__(self, c_h: float, c_w: float, maze: MazeGrid, maze_structure: dict[tuple[float, ...]: int]):
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = maze.height
        self.__m_w = maze.width
        self.__struct  = maze_structure


    @staticmethod
    def get_the_bit(value: int, direction: int) -> int:
        match direction:
            case "N":
                return (value >> 3) & 1
            case "E":
                return (value >> 2) & 1
            case "S":
                return (value >> 1) & 1
            case "W":
                return (value >> 0) & 1

    def print_top_line(self, cell: tuple[float, ...], wall: int) -> None:
        line : str = ""
        if cell[0] == 0 and cell[1] == 0 :
            line = line + Char.LT
        elif cell[1] == 0 and cell[0] != 0:
            if self.get_the_bit(wall, "W") == 0:
                line = line + Char.JT
        for i in range(self.__c_w):
            line = line + Char.H
        if cell[0] ==  self.__m_w - 1 and cell[1] == 0 :
            line = line + Char.RT
            line = line + "\n"
        print(line, end="")
    
    def print_middleline(self, cell: tuple[float, ...], wall: int) -> None:
        line: str = ""
        if cell[0] == 0 or cell[0] == self.__m_w - 1:
            line = line + Char.V
        for i in range(self.__c_w):
            line = line + " "
        print(line, end="")

    def visu(self) -> None:
        i: int = 0
        #for x in range(self.__m_h):
        for x in range(1):
            # new dict (cell): wall
            new_dict = {cell:self.__struct.get(cell) for cell in self.__struct if cell[1] == x}
            print(new_dict)
            for cell in new_dict:
                #bit : int = self.get_the_bit(new_dict.get(cell),y)
                # match y:
                #     case 3:
                #         s = "N"
                #     case 2:
                #         s = "E"
                #     case 1:
                #         s = "S"
                #     case 0:
                #         s = "W"
                ##print (f"cell:{cell}, bit: {format(new_dict.get(cell),'b')}, wall: {s},  {"WALL" if bit == 0 else "NO WALL"}")
                self.print_top_line(cell, new_dict.get(cell))
            for cell in new_dict:
                self.print_middleline(cell, new_dict.get(cell))
                
                


def get_bits(cell: tuple[float, ...], open_neighbors: list[Cell]) -> int :


    nord: tuple[float, ...] = (cell[0] , cell[1] - 1) 
    est: tuple[float, ...] = (cell[0] + 1 , cell[1]) 
    sud: tuple[float, ...] = (cell[0] , cell[1] + 1)
    west: tuple[float, ...] = (cell[0] - 1 , cell[1])

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
        value = value | (1 << 0)
    #this mask active the second bit for the South wall
    # if the South variable tuple is on neighbour list this bit is activate
    if sud in open_neighbors:
        value = value | (1 << 1)
    #this mask active the third bit for the Est wall
    # if the Est variable tuple is on neighbour list this bit is activate
    if est in open_neighbors:
        value = value | (1 << 2)
    #this mask active the fourth bit for the Nord wall
    # if the Nord variable tuple is on neighbour list this bit is activate
    if nord in open_neighbors:
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
    

    # i = 6

    # print(format(i, 'b'))
    # print((i >> 0) & 1)
    # print((i >> 1) & 1)
    # print((i >> 2) & 1)
    # print((i >> 3) & 1)
    
    
    i : int = 0
    maze_struct: dict[tuple[float, ...]: int] = get_output(maze)
    new_dict = {cell:maze_struct.get(cell) for cell in maze_struct if cell[1] == 0}
    # for o in maze_struct:
    #     print(f"cell: {o}, wall: {maze_struct.get(o), format(maze_struct.get(o), 'b')}, neighbour: {maze.graph.get(o)}")

    visu: Visualisation = Visualisation(10,10, maze, maze_struct)
    visu.visu()


    # print(maze.width)
    
