from collections import defaultdict
from typing import DefaultDict, Iterable, List, Tuple

Cell = Tuple[int, int]


class MazeValidationError(ValueError):
    """Raised when a maze graph structure is invalid."""


class MazeGrid:
    """A simple grid maze represented by an adjacency list.

    This class assumes width, height, and cell coordinates are already
    validated by the caller.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.graph: DefaultDict[Cell, List[Cell]] = defaultdict(list)
        self._initialize_cells()

    def _initialize_cells(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.graph[(x, y)] = []

    def in_bounds(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def is_adjacent(self, a: Cell, b: Cell) -> bool:
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def add_edge(self, a: Cell, b: Cell) -> None:
        if not self.in_bounds(a):
            raise MazeValidationError(f"Cell {a} is out of bounds")
        if not self.in_bounds(b):
            raise MazeValidationError(f"Cell {b} is out of bounds")
        if a == b:
            raise MazeValidationError("Cannot add self-loop edge")
        if not self.is_adjacent(a, b):
            raise MazeValidationError(
                f"Cells {a} and {b} are not adjacent"
            )
        if b not in self.graph[a]:
            self.graph[a].append(b)
        if a not in self.graph[b]:
            self.graph[b].append(a)

    def neighbors(self, cell: Cell) -> List[Cell]:
        if not self.in_bounds(cell):
            raise MazeValidationError(f"Cell {cell} is out of bounds")
        return list(self.graph[cell])

    def all_cells(self) -> Iterable[Cell]:
        return tuple(self.graph.keys())

    def validate(self) -> None:
        for cell, neighbors in self.graph.items():
            if not self.in_bounds(cell):
                raise MazeValidationError(f"Invalid cell {cell}")
            if len(neighbors) != len(set(neighbors)):
                raise MazeValidationError(f"Duplicate edges for {cell}")
            for neighbor in neighbors:
                if not self.in_bounds(neighbor):
                    raise MazeValidationError(
                        f"Neighbor {neighbor} of {cell} is out of bounds"
                    )
                if not self.is_adjacent(cell, neighbor):
                    raise MazeValidationError(
                        f"Neighbor {neighbor} of {cell} is not adjacent"
                    )
                if cell not in self.graph[neighbor]:
                    raise MazeValidationError(
                        f"Edge from {cell} to {neighbor} is not symmetric"
                    )

    def carve_passage(self, cell: Cell, neighbor: Cell) -> None:
        self.add_edge(cell, neighbor)

    def __repr__(self) -> str:
        return (
            f"MazeGrid(width={self.width}, height={self.height}, "
            f"edges={sum(len(v) for v in self.graph.values()) // 2})"
        )


def main() -> None:
    maze = MazeGrid(4, 3)
    maze.carve_passage((0, 0), (1, 0))
    maze.carve_passage((1, 0), (1, 1))
    maze.validate()
    print(maze)
    print("Neighbors of (1,0):", maze.neighbors((1, 0)))


if __name__ == '__main__':
    main()
