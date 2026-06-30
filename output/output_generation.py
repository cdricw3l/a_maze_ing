from mazegen.mazegen import Cell, Graph, MazeGrid
from typing import List
from visualisation.color import Color_line


class Output_creation_error(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class Output:

    __graph: Graph
    __entry: Cell
    __exit: Cell
    __shortest_path: dict[Cell, str]
    __maze_structure: dict[Cell, int]

    def __init__(self,
                 graph: Graph, entry: Cell, exit: Cell) -> None:
        if graph is None:
            raise Output_creation_error("Output file creation error: no graph")
        self.__graph = graph
        self.__entry = entry
        self.__exit = exit
        self.__maze_structure = self.get_maze_structure()
        self.__shortest_path = {}

    def set_shortest_path(self, path: dict[Cell, str]) -> None:
        self.__shortest_path = {k: path[k] for k in path}

    def get_shortest_path(self) -> dict[Cell, str]:
        return self.__shortest_path

    def _bytes_direction_activation(self,
                                    cell: tuple[float, float],
                                    open_neighbors: List[Cell]
                                    ) -> int:
        """Take a cell and its list of neighbors as parameters.
        Set the direction bit corresponding to any direction
        that is not present in the list of neighbors."""

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

    def get_direction(self, current: Cell, neighbour: Cell | None) -> str:
        """
            This methode  return the cardinal direction
            between current and neigbour
            For matching reason with the bfs alorithme,
            the return value is reversed
            Nord becomme south, East become west
        """

        if current is not None and neighbour is not None:
            if neighbour[0] == current[0] and neighbour[1] == current[1] - 1:
                return "S"
            if neighbour[0] == current[0] and neighbour[1] == current[1] + 1:
                return "N"
            if neighbour[0] == current[0] + 1 and neighbour[1] == current[1]:
                return "W"
            if neighbour[0] == current[0] - 1 and neighbour[1] == current[1]:
                return "E"
        return ""

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
        graph: Graph = self.__graph
        output: dict[tuple[int, int], int] = {}
        for cell in graph:
            open_neighbors: list[Cell] | None = graph.get(cell)
            if open_neighbors is None:
                raise Output_creation_error("Output file creation error")
            key: Cell = cell
            value: int = self._bytes_direction_activation(key, open_neighbors)
            output.update({key: value})
        return output

    def bfs_algorithm(
            self,
            maze: MazeGrid,
            current: Cell,
            exit: Cell) -> None:
        """
        This algorithm called breadth first search uses a queue to visit all
        possible paths and when the end is hit, get back via a path tracker
        """

        visited: set[Cell] = maze.forty_two_logo(maze.width, maze.height)
        visited.add(current)
        queue: list[Cell] = [current]
        parent: dict[Cell, Cell | None] = {current: None}
        while queue:
            current = queue.pop(0)
            if current == exit:
                break
            for neighbor in maze.neighbors(current):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
        path: dict[Cell, str] = {}
        curr: Cell | None = exit
        while curr is not None:
            path.update({curr: self.get_direction(curr, parent.get(curr))})
            curr = parent.get(curr)
        self.set_shortest_path(path)

    def write_output_file(self, maze_height: int) -> None:
        """
            This method allows you to output the maze representation,
            in hexadecimal format,
            the entry point, the exit point,
            and the shortest path between these two points.
        """
        # structure is a dict where:
        # the cell is the key and
        # the value is an interger
        # who descripte the cell structure (1001)
        structure: dict[Cell, int] = self.__maze_structure
        try:
            with open("output_maze.txt", 'w') as f:
                for i in range(maze_height):
                    row: list[str] = [format(structure.get(x), 'X')
                                      for x in structure if x[1] == i]
                    row.append('\n')
                    f.write("".join(row))
                f.write(f"\n{self.__entry[0], self.__entry[1]}\n")
                f.write(f"{self.__exit[0], self.__exit[1]}\n")
                path: str = "".join([
                    self.get_shortest_path()[k]
                            for k in self.get_shortest_path()])
                f.write(f"{path[::-1]}\n")
        except Exception as e:
            raise Output_creation_error(f"{Color_line.RED}"
                                        f"Output file creation error: {e}"
                                        f"{Color_line.RESET}")
