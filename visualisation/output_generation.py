from maze_generator.maze import Cell, Graph, MazeGrid
from typing import List
import sys

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
        sys.setrecursionlimit(1500)

    def set_shortest_path(self, path: dict[Cell, str]) -> None:
        self.__shortest_path = {k: path[k] for k in path}

    def get_shortest_path(self) -> dict[Cell, str]:
        return self.__shortest_path
    
    @staticmethod
    def get_len_path(path: dict[Cell, str]) -> int:
        i: int = len({i for i in path})
        return i
    
    def _bytes_direction_activation(self,
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
    
    def get_direction(self, current: Cell, neighbour: Cell) -> str:
        """ This fonction  return the cardinal direction between current and neigbour"""

        if current  is not None and neighbour is not None:
            if neighbour[0] == current[0] and neighbour[1] == current[1] - 1:
                return "N"
            if neighbour[0] == current[0] and neighbour[1] == current[1] + 1:
                return "S"
            if neighbour[0] == current[0] + 1 and neighbour[1] == current[1]:
                return "E"
            if neighbour[0] == current[0] - 1 and neighbour[1] == current[1]:
                return "W"
        return ""

    # def is_valide_move(self, current: Cell, neigbour: Cell, maze_structure: dict[Cell, int]) -> bool:
    #     """ This fonction check if the wall between two cell is open """
    #     # get the direction fron current to neigbour (WSEN)
    #     direction: str = self.get_direction(current, neigbour)
    #     # get the (WSEN) stucture of the cell
    #     wall: int = maze_structure.get(current)
    #     if direction == "W" and ((wall >> 3) & 1) == 0:
    #         return True
    #     if direction == "S" and ((wall >> 2) & 1) == 0:
    #         return True
    #     if direction == "E" and ((wall >> 1) & 1) == 0:
    #         return True
    #     if direction == "N" and ((wall >> 0) & 1) == 0:
    #         return True
    #     return False

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

    def bfs_algorithm(self, maze: MazeGrid, current: Cell, exit: Cell) -> dict[Cell, str]:
        """
        This algorithm called breadth first search uses a queue to visit all
        possible paths and when the end is hit, get back via a path tracker
        """

        visited: set[Cell] = maze.forty_two_logo(maze.width, maze.height)
        visited.add(current)
        queue: list[Cell] = [current]
        parent: dict[Cell, Cell] = {current: None}
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
        curr: Cell = exit
        while curr is not None:
            path.update({curr: self.get_direction(curr, parent.get(curr))})
            curr = parent.get(curr)
        #path.reverse()
        return path

    def _shortest_path_algo(self,
                            current: Cell,
                            neighbour: list[Cell] | None,
                            visited: list[Cell],
                            path: dict[Cell, str]) -> bool:
        
        if neighbour is not None and len(neighbour) == 0:
            return False
    
        if current == self.__exit:
            if self.get_len_path(self.__shortest_path) == 0 or self.get_len_path(path) < self.get_len_path(self.__shortest_path):
                print(f"path update new: {self.get_len_path(path)} old: {self.get_len_path(self.__shortest_path)}")
                self.set_shortest_path(path)
            return False
        visited.append(current)
        for cell in neighbour:
            if cell not in visited:

                direction = self.get_direction(current, cell)
                # print(f"string {string}")
                path.update({cell: direction})
                new_neighbour: list[Cell] | None = self.__graph.get(cell)
                if new_neighbour is None:
                    return False
                self._shortest_path_algo(cell,
                                            new_neighbour,
                                            visited,
                                            path)
                # print(f"delete char {string}")
                path.popitem()
                #visited.pop()
                #print(f"visited: {visited}")
        return True


    def shortest_path_generation(self, maze: MazeGrid) -> bool:
        entry = self.__entry
        exit = self.__exit
        #visited: list[Cell] = []
        #neighbour: list[Cell] | None = self.__graph.get(current)
        path: dict[Cell, str] = {}
        
        # if map_height > 40 and map_width > 40:
        #     sys.setrecursionlimit(sys.getrecursionlimit() + 500)
        # if neighbour is None:
        #     raise Output_creation_error(
        #         f"Output file creation error: "
        #         f"cant't found neighbour of the cell: {current}")
        try:
            shortest_path: dict[Cell, str] = self.bfs_algorithm(maze ,entry, exit)
            self.set_shortest_path(shortest_path)
            # for s in shortest_path:
            #     print(f"cell: {s} direction: {shortest_path.get(s)}" )
        except (RecursionError) as e:
            print(f"{e}")
            # if an Recurtion error occure, setrecursionlimit is increase
            # and the fonction return false. The fonction is recall until she return true.
            sys.setrecursionlimit(sys.getrecursionlimit() + 500)
            return False
        return True

    def write_output_file(self, maze_height: int) -> None:
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
                print(path)
                f.write(f"{path}\n")
        except Exception as e:
            raise Output_creation_error(f"Output file creation error: {e}")

if __name__ == "main":
    print(0 >> 0 & 1)