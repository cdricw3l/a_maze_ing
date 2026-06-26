from maze_generator.maze import MazeGrid, Cell
from .color import Color_bg
from collections import defaultdict
from typing import List, Set


Vertice_adjacent = dict[tuple[int, ...]: list[tuple[int, ...]]]
Vertice_char = dict[tuple[int, int], str]


class Char_set:

    __char_set: dict[str, str]

    def __init__(self) -> None:
        self.__char_set: dict[str, str] = {
            "NESW": "╋", "NES": '┣', "NEW": '┻',
            "NSW": '┫', "ESW": '┳', "NE": '┗',
            "NS": '┃', "NW": '┛', "ES": '┏',
            "EW": '━', "SW": '┓', "N": '╹',
            "E": '╺', "S": '╻', "W": '╸'}

    def get_char(self, code: str) -> str | None:
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
    __color: str
    __forty_two_color: str
    __reset: str

    def __init__(
            self,
            c_h: float,
            c_w: float,
            maze: MazeGrid,
            maze_structure: dict[tuple[float, ...]: int],
            forty_two: Set[Cell],
            color: str = "\033[0m",
            forty_two_color: str = "\033[45m"
            ) -> None:
        super().__init__()
        self.__c_h = c_h
        self.__c_w = c_w
        self.__m_h = maze.height
        self.__m_w = maze.width
        self.__entry = maze.entry
        self.__exit = maze.exit
        self.__forty_two = forty_two
        self.__struct = maze_structure
        self.__color = color
        self.__forty_two_color = forty_two_color
        self.__reset = "\033[0m"

    def vertice_dict(self) -> dict[tuple[int]: list[tuple[int, ...]]]:
        """
            create a dict of vertice (jonction point of the cell )
            and match the vertice point whith 2 oposed adjoining rooms
            (Nord-west/ Sud-east) see the read me.
            The number of vertice = maze_width + 1 * maze_height + 1
        """
        vertice: dict[tuple[int, ...]: list[tuple[int, ...]]] = {}
        for x in range(self.__m_h + 1):
            for y in range(self.__m_w + 1):
                cell: tuple[int, int] = (y, x)
                nw: tuple[int, int] = (y - 1, x - 1)
                se: tuple[int, int] = (y, x)
                vertice.update({cell: list([nw, se])})
        return vertice

    def check_if_open(self,
                      adjoining_rooms: tuple[int, int],
                      adjacent_cell: tuple[int, int],
                      direction: str) -> str:
        room_bit: int = self.__struct.get(adjoining_rooms)
        adjacent_cell_bit: int = self.__struct.get(adjacent_cell)

        # print(f"room: {adjoining_rooms,room_bit},"
        # f"adjacent cell: {adjacent_cell, adjacent_cell_bit}"
        # f"position: {direction}")

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

    def get_vertice_char(self, adjoining_rooms: List[tuple[int, int]]) -> str:

        v: str = ""
        w_cell: tuple[int, int] = tuple(
            [adjoining_rooms[0][0],
             adjoining_rooms[0][1] + 1])
        n_cell: tuple[int, int] = tuple(
            [adjoining_rooms[0][0] + 1,
             adjoining_rooms[0][1]])
        e_cell: tuple[int, int] = tuple(
            [adjoining_rooms[1][0],
             adjoining_rooms[1][1] - 1])
        s_cell: tuple[int, int] = tuple(
            [adjoining_rooms[1][0] - 1,
             adjoining_rooms[1][1]])

        # print(f"adjoining root: {adjoining_rooms}")
        # print(f"vertice: {vertice}, "
        # f"w: {w_cell}, "
        # f"n: {n_cell}, "
        # f"e: {e_cell}, "
        # f"s: {s_cell}")

        nord: str = self.check_if_open(adjoining_rooms[0], n_cell, "N")
        v = v + nord
        east: str = self.check_if_open(adjoining_rooms[1], e_cell, "E")
        v = v + east
        south: str = self.check_if_open(adjoining_rooms[1], s_cell, "S")
        v = v + south
        west: str = self.check_if_open(adjoining_rooms[0], w_cell, "W")
        v = v + west
        return self.get_char(v)

    def add_char(self, char: str, number: int, color: str) -> str:
        line: str = f"{color}"
        for i in range(number):
            line = line + char
        line = line + f"{self.__reset}"
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

    def is_on_horizontal_set(self, char: str) -> bool:
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
            line = line + f"{self.__color}{vertices.get(v)}{self.__reset}"
            if v[0] != self.__m_w:
                if self.is_on_horizontal_set(vertices.get(v)):
                    line = line + self.add_char(
                        Char_set.get_char(self, "EW"),
                        self.__c_w - 2,
                        self.__color)
                else:
                    line = line + self.add_char(
                        " ",
                        self.__c_w - 2,
                        self.__color)
        print(line)

    def create_v_line(self, vertices: dict[tuple[int, ...], str]) -> None:
        line: str = ""
        for v in vertices:
            if self.is_on_vertical_set(vertices.get(v)):
                line = line + \
                    f"{self.__color}" \
                    f"{Char_set.get_char(self, 'NS')}" \
                    f"{self.__reset}"
            else:
                line = line + " "
            if v[0] != self.__m_w:
                if v == self.__entry:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.GREEN)
                elif v == self.__exit:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.RED)
                elif v in self.__forty_two:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, self.__forty_two_color)
                else:
                    line = line + self \
                        .add_char(" ", self.__c_w - 2, Color_bg.TRANSPARANT)
        print(line)

    def display_maze(self) -> None:
        vertices_adjacent: Vertice_adjacent = self.vertice_dict()
        vertices_char: Vertice_char = {}
        for vertice in vertices_adjacent:
            # print(f"{vertice}, ajoining :{vertices.get(vertice)}")
            charactere: str = self \
                .get_vertice_char(vertices_adjacent.get(vertice))
            vertices_char.update({vertice: charactere})

        for i in range(self.__m_h + 1):
            new_v: dict[tuple[int, int], str] = \
                {k: vertices_char[k] for k in vertices_char if k[1] == i}
            self.create_h_line(new_v)
            for j in range(3):
                self.create_v_line(new_v)

    def set_bg_color(self, color: str) -> None:
        self.__forty_two_color = color

    def set_line_color(self, color: str) -> None:
        self.__color = color


def bytes_direction_activation(
        cell: tuple[float, float],
        open_neighbors: List[Cell]
        ) -> int:

    west: tuple[float, float] = (cell[0] - 1, cell[1])
    sud: tuple[float, float] = (cell[0], cell[1] + 1)
    est: tuple[float, float] = (cell[0] + 1, cell[1])
    nord: tuple[float, float] = (cell[0], cell[1] - 1)

    # the binary value of 0 is 0000
    value: int = 0

    # this mask active the first bit for the West wall
    # if the West variable tuple is not on open neighbour list
    # this bit is activate the wall is closed an value
    if west not in open_neighbors:
        value = value | (1 << 3)
    # this mask active the second bit for the South wall
    # if the South variable tuple is not on open neighbour list
    # this bit is activate the wall is closed
    if sud not in open_neighbors:
        value = value | (1 << 2)
    # this mask active the third bit for the Est wall
    # if the Est variable tuple is on open neighbour list
    # this bit is activate the wall is closed
    if est not in open_neighbors:
        value = value | (1 << 1)
    # this mask active the fourth bit for the Nord wall
    # if the Nord variable tuple is on open neighbour list
    # this bit is activate the wall is closed
    if nord not in open_neighbors:
        value = value | (1 << 0)

    return value


def get_output(maze: MazeGrid) -> dict[tuple[float,  float]: int]:

    """
    return a dict with cell coordonee as key and
    integer value who represente which wall is open
    exemple: WSEN -> 0100:
    West is open, south is closed, east is open and nord is open
    exemple: WSEN -> 0000:
    all the wall are open
    exemple: WSEN -> 1111:
    all the wall are closed
    """
    graph: defaultdict[Cell, List[Cell]] = maze.graph
    output: dict[tuple[float, ...]: int] = {}
    for cell in graph:
        open_neighbors: list[Cell] = graph.get(cell)
        key: tuple[float, ...] = cell
        value: int = bytes_direction_activation(key, open_neighbors)
        output.update({key: value})
    return output


def visualisation_maze(
        maze: MazeGrid,
        line_color,
        forty_two_color: str = "\033[45m"
        ) -> None:

    forty_two: set[Cell] = maze.forty_two_logo(maze.width, maze.height)
    output: dict[tuple[float, float]: int] = get_output(maze)
    visualiser: Visualisation = Visualisation(
        10, 10,
        maze, output,
        forty_two, line_color,
        forty_two_color
    )
    visualiser.display_maze()
