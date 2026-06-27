from maze_generator.maze import Cell
from typing import List
from collections import defaultdict


class Output_creation_error(Exception):
    def __init__(self) -> None:
        super().__init__("Output file creation error")


class Output:

    __graph: defaultdict[Cell, List[Cell]]

    def __init__(self, graph: defaultdict[Cell, List[Cell]]) -> None:
        if graph is None:
            raise Output_creation_error
        self.__graph = graph

    def bytes_direction_activation(self,
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

    def get_maze_structure(self) -> dict[Cell, int]:

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
        graph: defaultdict[Cell, List[Cell]] = self.__graph
        output: dict[tuple[int, int], int] = {}
        for cell in graph:
            open_neighbors: list[Cell] | None = graph.get(cell)
            if open_neighbors is None:
                raise Output_creation_error
            key: Cell = cell
            value: int = self.bytes_direction_activation(key, open_neighbors)
            output.update({key: value})
        return output
