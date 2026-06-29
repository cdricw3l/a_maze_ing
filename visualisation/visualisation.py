from maze_generator.maze import MazeGrid, Cell
from .color import Color_bg
from .output_generation import Output_creation_error, Output
from typing import List, Set

Vertex_char = dict[Cell, str]
Vertex = dict[Cell, list[Cell]]


class Vertex_creation_error(Exception):
    def __init__(self, msg: str ="Error vertex contruction set") -> None:
        super().__init__(msg)


class Display_creation_error(Exception):
    def __init__(self, msg: str ="Display creation error") -> None:
        super().__init__(msg)


class Char_set:

    __char_set: dict[str, str]

    def __init__(self) -> None:
        self.__char_set: dict[str, str] = {
            "NESW": "╋", "NES": '┣', "NEW": '┻',
            "NSW": '┫', "ESW": '┳', "NE": '┗',
            "NS": '┃', "NW": '┛', "ES": '┏',
            "EW": '━', "SW": '┓', "N": '╹',
            "E": '╺', "S": '╻', "W": '╸', "": ' '}

    def get_char(self, code: str) -> str | None:
        return self.__char_set.get(code)


class Direction:
    WEST: int = 3
    SOUTH: int = 2
    EAST: int = 1
    NORD: int = 0


class Visualisation(Char_set):
    __c_w: int
    __c_h: int
    __m_h: int
    __m_w: int
    __entry: tuple[int, int]
    __exit: tuple[int, int]
    __shortest_path: dict[Cell, str]
    __struct: dict[Cell, int]
    __color: str
    __forty_two_color: str
    __path_color: str
    __reset: str
    __path_state: bool

    def __init__(
            self,
            c_h: int,
            c_w: int,
            maze: MazeGrid,
            maze_structure: dict[Cell, int],
            shortest_path: dict[Cell, str],
            forty_two: Set[Cell],
            color_line: str,
            forty_two_color: str,
            shortest_path_color: str,
            path_state: bool
            ) -> None:
        super().__init__()
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = maze.height
        self.__m_w = maze.width
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__shortest_path = shortest_path
        self.__forty_two = forty_two
        self.__struct = maze_structure
        self.__color = color_line
        self.__forty_two_color = forty_two_color
        self.__path_color = shortest_path_color
        self.__path_state = path_state
        self.__reset = "\033[0m"

    def set_bg_color(self, color: str) -> None:
        self.__forty_two_color = color

    def set_line_color(self, color: str) -> None:
        self.__color = color

    def vertex_dict(self) -> Vertex:
        """
            create a dict of vertice (jonction point of the cell )
            and match the vertice point whith 2 oposed adjoining rooms
            (Nord-west/ Sud-east) see the read me.
            The number of vertice = maze_width + 1 * maze_height + 1
        """
        vertice: Vertex = {}
        for x in range(self.__m_h + 1):
            for y in range(self.__m_w + 1):
                cell: tuple[int, int] = (y, x)
                nw: tuple[int, int] = (y - 1, x - 1)
                se: tuple[int, int] = (y, x)
                vertice.update({cell: list([nw, se])})
        return vertice

    def check_if_open(self,
                      adjoining_rooms: Cell,
                      adjacent_cell: Cell,
                      direction: str) -> str:
        room_bit: int | None = self.__struct.get(adjoining_rooms)
        adjacent_cell_bit: int | None = self.__struct.get(adjacent_cell)

        if room_bit is None and adjacent_cell_bit is None:
            return ""
        if room_bit is None or adjacent_cell_bit is None:
            return direction
        if direction == "W":
            # comparaison nord room_bit -> south ajacent cell give w
            if ((room_bit >> Direction.SOUTH) & 1) == 1\
                and\
                    ((adjacent_cell_bit >> Direction.NORD) & 1) == 1:
                return "W"
        if direction == "S":
            # comparaison WEST room_bit -> EAST ajacent cell give s
            if ((room_bit >> Direction.WEST) & 1) == 1\
                and\
                    ((adjacent_cell_bit >> Direction.EAST) & 1) == 1:
                return "S"
        if direction == "E":
            # comparaison NORD room_bit -> SOUTH ajacent cell give E
            if ((room_bit >> Direction.NORD) & 1) == 1\
                and\
                    ((adjacent_cell_bit >> Direction.SOUTH) & 1) == 1:
                return "E"
        if direction == "N":
            # comparaison EAST room_bit -> WEST ajacent cell give N
            if ((room_bit >> Direction.EAST) & 1) == 1\
                and\
                    ((adjacent_cell_bit >> Direction.WEST) & 1) == 1:
                return "N"
        return ""

    def get_vertex_char(self,
                        adjoining_rooms: List[Cell] | None) -> str | None:

        if adjoining_rooms is None:
            raise Vertex_creation_error(
                f"adjoining_rooms are none {adjoining_rooms}")
        v: str = ""
        w_cell: Cell = (adjoining_rooms[0][0],
                        adjoining_rooms[0][1] + 1)
        n_cell: Cell = (adjoining_rooms[0][0] + 1,
                        adjoining_rooms[0][1])
        e_cell: Cell = (adjoining_rooms[1][0],
                        adjoining_rooms[1][1] - 1)
        s_cell: Cell = (adjoining_rooms[1][0] - 1,
                        adjoining_rooms[1][1])

        nord: str = self.check_if_open(adjoining_rooms[0], n_cell, "N")
        v = v + nord
        east: str = self.check_if_open(adjoining_rooms[1], e_cell, "E")
        v = v + east
        south: str = self.check_if_open(adjoining_rooms[1], s_cell, "S")
        v = v + south
        west: str = self.check_if_open(adjoining_rooms[0], w_cell, "W")
        v = v + west
        char: str | None = self.get_char(v)
        if char is None:
            raise Vertex_creation_error("get_vertex_char: error char creation")
        return char

    def add_char(self, char: str, number: int, color: str) -> str:
        line: str = f"{color}"
        for i in range(number):
            line = line + char
        line = line + f"{self.__reset}"
        return line

    def has_south_branch(self, vertex: str | None) -> bool:
        """
            Check if a vertex has a south branch.
        """
        if self.get_char("NESW") == vertex:
            return True
        elif self.get_char("NES") == vertex:
            return True
        elif self.get_char("NSW") == vertex:
            return True
        elif self.get_char("ESW") == vertex:
            return True
        elif self.get_char("NS") == vertex:
            return True
        elif self.get_char("ES") == vertex:
            return True
        elif self.get_char("SW") == vertex:
            return True
        elif self.get_char("S") == vertex:
            return True
        return False

    def has_east_branch(self, vertex: str | None) -> bool:
        """
            Check if a vertex has a east branch.
        """
        if self.get_char("NESW") == vertex:
            return True
        elif self.get_char("NES") == vertex:
            return True
        elif self.get_char("NEW") == vertex:
            return True
        elif self.get_char("ESW") == vertex:
            return True
        elif self.get_char("NE") == vertex:
            return True
        elif self.get_char("ES") == vertex:
            return True
        elif self.get_char("EW") == vertex:
            return True
        elif self.get_char("E") == vertex:
            return True
        return False

    def create_vertex_set(self, vertex_adjacent: Vertex) -> Vertex_char:
        """
            return dict of {vertice: charactere}:
            exemple {(0,0):┏}
        """
        vertex_char: Vertex_char = {}
        for vertex in vertex_adjacent:
            # print(f"{vertice}, ajoining :{vertices.get(vertice)}")
            character: str | None = self \
                .get_vertex_char(vertex_adjacent.get(vertex))
            if character is None:
                raise Vertex_creation_error(f"{character}")
            vertex_char.update({vertex: character})
        return vertex_char

    def vertex_line(self, vertex: dict[Cell, str]) -> str:
        """
            vertice line creation create line
            with vertices charactere and complement id needed
        """
        line: str = ""
        for v in vertex:
            # firt caractere of the vertice (0,0)
            line = line + f"{self.__color}{vertex.get(v)}{self.__reset}"
            # complete line for vertice
            # from (0,y) to vertice (self.__m_w - 1, y)
            if v[0] != self.__m_w:
                # if vertice has east branch, add (cell with - 2) EW char
                if self.has_east_branch(vertex.get(v)):
                    vertice_char: str | None = Char_set.get_char(self, "EW")
                    if vertice_char is None:
                        raise Vertex_creation_error("vertex_line error")
                    line = line + self.add_char(
                        vertice_char,
                        self.__c_w - 2,
                        self.__color)
                # if vertice doest have east branch,
                # add (cell with - 2) space char
                else:
                    line = line + self.add_char(
                        " ",
                        self.__c_w - 2,
                        self.__color)
        line = line + '\n'
        return line

    def inter_vertex_line(self, vertex: dict[Cell, str]) -> str:
        """ inter vertices creation line """
        line: str = ""
        for v in vertex:
            # check if the vertice has a south branch.
            # if true add NS charactere
            if self.has_south_branch(vertex.get(v)):
                jonction: str | None = Char_set.get_char(self, 'NS')
                if jonction is None:
                    raise Vertex_creation_error("here")
                line = line + \
                    f"{self.__color}" \
                    f"{jonction}" \
                    f"{self.__reset}"
            # if the vertice hasn't a south branch.
            # add space charactere
            else:
                line = line + " "
            # complete line for vertice from (0,y)
            # to vertice (self.__m_w - 1, y)
            # The color of the space depend of the cell type
            # (entry, exit, 42, shortest path)
            if v[0] != self.__m_w:
                # color the entry background
                if v == self.__entry:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.GREEN)
                # color the exit background
                elif v == self.__exit:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.RED)
                # color the 42 logo background
                elif v in self.__forty_two:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, self.__forty_two_color)
                elif v in self.__shortest_path and self.__path_state is True:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, self.__path_color)
                else:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.TRANSPARANT)
        line = line + '\n'
        return line

    def display_maze(self) -> None:
        vertices_adjacent: Vertex = self.vertex_dict()
        vertices_char: Vertex_char = {}
        line: str = ""
        try:
            vertices_char = self.create_vertex_set(vertices_adjacent)
            for i in range(self.__m_h + 1):
                new_v: dict[Cell, str] = \
                    {k: vertices_char[k] for k in vertices_char if k[1] == i}
                line = line + self.vertex_line(new_v)
                line = line + self.inter_vertex_line(new_v)
        except Vertex_creation_error as e:
            raise Display_creation_error(f"Vertex creation error: {e}")
        print(line)


def visualisation_maze(
        maze: MazeGrid,
        line_color: str,
        forty_two_color: str,
        shortest_path_color: str,
        path_state: bool
        ) -> bool:

    forty_two: set[Cell] = maze.forty_two_logo(maze.width, maze.height)
    try:
        output: Output = Output(maze.graph, maze.entry, maze.exit)
        maze_structure: dict[Cell, int] = output.get_maze_structure()
        output.bfs_algorithm(maze, maze.entry, maze.exit)
        visualiser: Visualisation = Visualisation(
            5, 6,
            maze, maze_structure, output.get_shortest_path(),
            forty_two, line_color,
            forty_two_color, shortest_path_color, path_state
        )
        visualiser.display_maze()
        output.write_output_file(maze.height)
        return True
    except (Output_creation_error, Display_creation_error) as e:
        print(e)
        return False
