from amazing.maze_generator.maze import MazeGrid, Cell
from collections import defaultdict
from typing import DefaultDict, Iterable, List, Tuple, Set, Optional, Literal

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


class Char_set:
    # LT: typing.Literal[True] = '╔'
    # LB: typing.Literal[True] = '╚' 
    # RT: typing.Literal[True] = '╗' 
    # RB: typing.Literal[True] = '╝' 
    # JT: typing.Literal[True] = '╦'
    # JB: typing.Literal[True] = '╩'
    # JL: typing.Literal[True] = '╠'
    # JR: typing.Literal[True] = '╣'
    # JM: typing.Literal[True] = '╬'
    # H: typing.Literal[True] = '═'
    # V: typing.Literal[True] = '║'
    
    __char_set: dict[str,str]
    def __init__(self):
        self.__char_set: dict[str,str] = {
            "NESW" : "┼", "NES" :'├', "NEW" :'┴', "NSW": '┤', "ESW": '┬', "NE": '└',
            "NS": '│', "NW": '┘', "ES": '┌', "EW": '─', "SW": '┐', "N": '╵', "E":'╶',
            "S": '╷',"W":'╴', "EMPTY": '.'}

    def get_char(self, code: str) -> str:
        return self.__char_set.get(code)

class Direction:
    WEST: int = 3
    SOUTH: int = 2
    EAST: int = 1
    NORD: int = 0

class Visualisation(Char_set):
    __c_w: float
    __c_h: float
    __m_h: float
    __m_w: float
    __entry: tuple[int, int]
    __exit: tuple[int, int]
    __struct: dict[tuple[float, ...]: int]

    def __init__(self, c_h: float, c_w: float, maze: MazeGrid, maze_structure: dict[tuple[float, ...]: int], forty_two: Set[Cell]):
        super().__init__()
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = maze.height
        self.__m_w = maze.width
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__forty_two = forty_two
        self.__struct  = maze_structure

    def vertice_dict(self) -> dict[tuple[int]: list[tuple[int, ...]]]:
        """ 
            create a dict of vertice (jonction point of the cell ) and match the vertice point whith 2 oposed adjoining rooms (Nord-west/ Sud-east) see the read me.
            The number of vertice = maze_width + 1 * maze_height + 1
        
        """
        vertice: dict[tuple[int, ...]: list[tuple[int, ...]]] = {}
        for x in range(self.__m_h + 1):
            for y in range(self.__m_w + 1):
                cell: tuple[int, ...] = (y, x)
                nw: tuple[int, ...] = (y - 1 , x -1)
                se: tuple[int, ...] = (y , x)
                vertice.update({cell:list([nw, se])})
        return vertice
    
    def check_if_open(self, adjoining_rooms: tuple[int, ...], adjacent_cell:tuple[int, ...], direction: str):
        room_bit: int = self.__struct.get(adjoining_rooms)
        adjacent_cell_bit: int = self.__struct.get(adjacent_cell)

        #print(f"room: {adjoining_rooms,room_bit}, adjacent cell: {adjacent_cell, adjacent_cell_bit} position: {direction}")

        if room_bit == None and adjacent_cell_bit == None:
             return ""
        if room_bit == None or adjacent_cell_bit == None:
             return direction
        if direction == "W":
                #comparaison nord room_bit -> south ajacent cell give w
                if ((room_bit >> Direction.SOUTH) & 1 ) == 1 and ((adjacent_cell_bit >> Direction.NORD) & 1) == 1:
                    return "W"
        if direction == "S":
                #comparaison WEST room_bit -> EAST ajacent cell give s
                if ((room_bit >> Direction.WEST) & 1 ) == 1 and ((adjacent_cell_bit >> Direction.EAST) & 1) == 1:
                    return "S"
        if direction == "E":
                #comparaison NORD room_bit -> SOUTH ajacent cell give E
                if ((room_bit >> Direction.NORD) & 1 ) == 1 and ((adjacent_cell_bit >> Direction.SOUTH) & 1) == 1:
                    return "E"
        if direction == "N":
                #comparaison EAST room_bit -> WEST ajacent cell give N
                if ((room_bit >> Direction.EAST) & 1 ) == 1 and ((adjacent_cell_bit >> Direction.WEST) & 1) == 1:
                    return "N"
        return ""
    
    
    def get_vertice_char(self, vertice: tuple[int, ...], adjoining_rooms: List[tuple[int, ...]])  -> str:
        
        v: str = ""
        w_cell: tuple[int] = tuple([adjoining_rooms[0][0], adjoining_rooms[0][1] + 1])
        n_cell: tuple[int, ...] = tuple([adjoining_rooms[0][0] + 1, adjoining_rooms[0][1]])
        e_cell: tuple[int] = tuple([adjoining_rooms[1][0] , adjoining_rooms[1][1] - 1])
        s_cell: tuple[int] = tuple([adjoining_rooms[1][0] - 1 , adjoining_rooms[1][1]])

        # print(f"adjoining root: {adjoining_rooms}")
        # print(f"vertice: {vertice}, w: {w_cell}, n: {n_cell}, e: {e_cell}, s: {s_cell}")
        
        
        nord: str = self.check_if_open(adjoining_rooms[0], n_cell, "N")
        v = v + nord
        east: str = self.check_if_open(adjoining_rooms[1], e_cell, "E")
        v = v + east
        south: str = self.check_if_open(adjoining_rooms[1], s_cell, "S")
        v = v + south
        west: str = self.check_if_open(adjoining_rooms[0], w_cell, "W")
        v = v + west
        return self.get_char(v)


    def add_char(self, char: str, number: int) -> str:
        line : str = ""
        for i in range(number):
            line = line + char
        return line

    def is_on_vertical_set(self, char: str) -> bool:
        if self.get_char("NESW") == char:
            return True
        elif self.get_char("NES") == char:
            return True
        elif self.get_char("NSW") == char:
            return True
        elif self.get_char("ESW") == char:
            return True
        elif self.get_char("NS") == char:
            return True
        elif self.get_char("ES") == char:
            return True
        elif self.get_char("SW") == char:
            return True
        elif self.get_char("S") == char:
            return True
        return False
    
    def is_on_horizontal_set(self, char:str) -> bool:
        if self.get_char("NESW") == char:
            return True
        elif self.get_char("NES") == char:
            return True
        elif self.get_char("NEW") == char:
            return True
        elif self.get_char("ESW") == char:
            return True
        elif self.get_char("NE") == char:
            return True
        elif self.get_char("ES") == char:
            return True
        elif self.get_char("EW") == char:
            return True
        elif self.get_char("E") == char:
            return True
        return False

    def create_h_line(self, vertices: dict[tuple[int, ...], str]) -> None:
        line: str = ""
        for v in vertices:
            line = line + vertices.get(v)
            if v[0] != self.__m_w:
                if self.is_on_horizontal_set(vertices.get(v)):
                    line = line + self.add_char("─", self.__c_w - 2)
                else:
                    line = line + self.add_char(" ", self.__c_w - 2)
        print(line)

    def create_v_line(self, vertices: dict[tuple[int, ...], str]) -> None:
        line: str = ""
        for v in vertices:
            if self.is_on_vertical_set(vertices.get(v)):
                line = line + "│"
            else:
                line = line + " "
            if v[0] != self.__m_w:
                if v == self.__entry:
                    line = line + self.add_char("\033[42m \033[00m", self.__c_w - 2)
                elif v == self.__exit:
                    line = line + self.add_char("\033[41m \033[00m", self.__c_w - 2)
                elif v in self.__forty_two:
                    line = line + self.add_char("\033[45m \033[00m", self.__c_w - 2)
                else:
                    line = line + self.add_char(" ", self.__c_w - 2)
        print(line)

    def display_maze(self) -> None:
        vertices_and_adjacent: dict[tuple[int, ...]: list[tuple[int, ...]]] = self.vertice_dict()
        vertices_and_char: dict[tuple[int, ...], str] = {}
        for vertice in vertices_and_adjacent:
            #print(f"{vertice}, ajoining :{vertices.get(vertice)}")
            charactere: str = self.get_vertice_char(vertice, vertices_and_adjacent.get(vertice))
            vertices_and_char.update({vertice:charactere})
        
        #for i in range(self.__m_h + 1):
        for i in range(self.__m_h + 1):
            new_v: dict[tuple[int, ...], str] = {k:vertices_and_char[k] for k in vertices_and_char if k[1] == i}
            self.create_h_line(new_v)
            assert(self.__c_h == 10)
            for j in range(3):
                self.create_v_line(new_v)

def bytes_direction_activation(cell: tuple[float, ...], open_neighbors: List[Cell]) -> int :


    west: tuple[float, ...] = (cell[0] - 1 , cell[1])
    sud: tuple[float, ...] = (cell[0] , cell[1] + 1)
    est: tuple[float, ...] = (cell[0] + 1 , cell[1]) 
    nord: tuple[float, ...] = (cell[0] , cell[1] - 1) 

    # the binary value of 0 is 0000
    value: int = 0

    #this mask active the first bit for the West wall
    # if the West variable tuple is not on open neighbour list this bit is activate the wall is closed an value
    if west not in open_neighbors:
        value = value | (1 << 3)
    #this mask active the second bit for the South wall
    # if the South variable tuple is not on open neighbour list this bit is activate the wall is closed
    if sud not in open_neighbors:
        value = value | (1 << 2)
    #this mask active the third bit for the Est wall
    # if the Est variable tuple is on open neighbour list this bit is activate the wall is closed
    if est not in open_neighbors:
        value = value | (1 << 1)
    #this mask active the fourth bit for the Nord wall
    # if the Nord variable tuple is on open neighbour list this bit is activate the wall is closed
    if nord not in open_neighbors:
        value = value | (1 << 0)

    return value
     

def get_output(maze: MazeGrid) -> dict[tuple[float,...]: int]:
    
    """ 
    return a dict with cell coordonee as key and 
    integer value who represente which wall is open 
    exemple: WSEN -> 0100 -> West is open, south is closed, east is open and nord is open
    exemple: WSEN -> 0000 -> all the wall are open 
    exemple: WSEN -> 1111 -> all the wall are closed 
    """
    graph: defaultdict[Cell, List[Cell]] = maze.graph
    output: dict[tuple[float, ...]: int] = {}
    for cell in graph:
        open_neighbors: list[Cell] = graph.get(cell)
        key: tuple[float, ...] = cell
        value: int = bytes_direction_activation(key, open_neighbors)
        output.update({key:value})
    
    return output



def visualisation_maze(maze: MazeGrid) -> None:
    
    forty_two: set[Cell] = maze.forty_two_logo(maze.width, maze.height)
    output: dict[tuple[float,...]: int] = get_output(maze)
    visualiser: Visualisation = Visualisation(10, 10, maze, output, forty_two)
    print(forty_two)
    visualiser.display_maze()
    
   