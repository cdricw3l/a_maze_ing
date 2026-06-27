from maze_generator.maze import Cell
from typing import List, IO
from collections import defaultdict


class Output_creation_error(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)



class Output:

    __graph: defaultdict[Cell, List[Cell]]
    __entry: Cell
    __exit: Cell
    __shortest_path: str
    __maze_structure: dict[Cell, int]

    def __init__(self, graph: defaultdict[Cell, List[Cell]], entry: Cell, exit: Cell) -> None:
        if graph is None:
            raise Output_creation_error("Output file creation error: no graph")
        self.__graph = graph
        self.__entry = entry
        self.__exit = exit
        self.__maze_structure = self.get_maze_structure()
    
    def set_shortest_path(self, path: str) -> None:
        self.__shortest_path = path

    def get_shortest_path(self) -> str:
        return str(self.__shortest_path)

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
                raise Output_creation_error("Output file creation error")
            key: Cell = cell
            value: int = self.bytes_direction_activation(key, open_neighbors)
            output.update({key: value})
        return output
    
    def get_direction(self, current: Cell, neighbour: Cell) -> str:
        if neighbour[0] == current[0] and neighbour[1] == current[1] - 1:
            return "N"
        if neighbour[0] == current[0] and neighbour[1] == current[1] + 1:
            return "S"
        if neighbour[0] == current[0] + 1 and neighbour[1] == current[1]:
            return "E"
        if neighbour[0] == current[0] - 1 and neighbour[1] == current[1]:
            return "W"
    
    def _shortest_path_algo(self,
                      current: Cell,
                      neighbour: list[Cell],
                      visited: list,
                      path) -> bool:

        if len(neighbour) == 0:
            return False
        if current == self.__exit:
            #print(f"sortie found: {len(string)} {current}")
            #print(f"path: {string}")
            self.set_shortest_path(path)
            return True
        
        #print(f"cell: {current} neighbour {neighbour}")
        visited.append(current)
        for cell in neighbour:
            if cell not in visited:

                path = path + self.get_direction(current, cell)
                #print(f"string {string}")
                self._shortest_path_algo(cell , self.__graph.get(cell), visited, path)
                #print(f"delete char {string}")
                path = path[:-1]
        return True

    def shortest_path(self) -> bool:
        current = self.__entry
        visited: list[Cell] = []
        neighbour: list[Cell] = self.__graph.get(current)
        path: str = ""
        try:
            self._shortest_path_algo(current, neighbour, visited, path)
        except RecursionError:
            raise Output_creation_error("Output file creation error: map to big for find the shortest_path")
    

    def write_output_file(self, maze_height: int) -> None:
        # structure is a dict where:
        # the cell is the key and
        # the value is an interger
        # who descripte the cell structure (1001)
        structure: dict[Cell, int] = self.__maze_structure

        try:
            with open("output_maze.txt", 'w') as f:
                
                for i in range(maze_height):
                    row: list[str] = [format(structure.get(x),'X') for x in structure if x[1] == i]
                    row.append('\n')
                    f.write("".join(row))
                f.write(f"\n{self.__entry[0], self.__entry[1]}\n")
                f.write(f"{self.__exit[0], self.__exit[1]}\n")
                f.write(f"{self.get_shortest_path()}")
        except Exception as e:
            raise Output_creation_error(f"Output file creation error: {e}")