from collections import defaultdict
from typing import DefaultDict, Iterable, List, Tuple, Set, Optional
from parsing.parse_config import Config, parse_config, ConfigError
import random
import sys

Cell = Tuple[int, int]


class MazeValidationError(ValueError):
    """Raised when a maze graph structure is invalid."""


class MazeGrid:
    """A simple grid maze represented by an adjacency list.

    This class assumes width, height, and cell coordinates are already
    validated by the caller.
    """

    def __init__(self, width: int, height: int, entry: Cell, exit: Cell) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
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

    def random_unvisited_neighbor(
        self,
        cell: Cell,
        visited: Set[Cell]
    ) -> Optional[Cell]:
        candidates: List[Cell] = []
        x, y = cell

        for neighbor in [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]:
            if not self.in_bounds(neighbor):
                continue
            if neighbor in visited:
                continue
            candidates.append(neighbor)

        if not candidates:
            return None

        return random.choice(candidates)

    @staticmethod
    def forty_two_logo(width: int, height: int) -> Set[Cell]:
        forbidden: set[Cell] = set()
        if width < 7 and height < 7:
            return forbidden
        x: int = int(width / 2)
        y: int = int(height / 2)
        forbidden = {
            (x+1, y),
            (x+2, y),
            (x-1, y), 
            (x-2, y),
            (x+1, y+2),
            (x+1, y-2),
            (x+2, y-1),
            (x+2, y+2),
            (x+1, y+1),
            (x+2, y-2),
            (x-1, y+2),
            (x-1, y+1), 
            (x-2, y-1),
            (x-2, y-2)
        }
        return forbidden

    def make_imperfect(self, percent: float = 0.05) -> None:
        """Add random passages to create alternative paths."""
        walls = [
            ((x, y), (nx, ny))
            for x in range(self.width)
            for y in range(self.height)
            for nx, ny in [(x+1, y), (x, y+1)]
            if self.in_bounds((nx, ny)) and (nx, ny) not in self.graph[(x, y)]
            and len(self.graph[(x, y)]) < 2
        ]

        if walls:
            num_to_remove = int(len(walls) * percent)
            if num_to_remove == 0:
                num_to_remove = 1
            for a, b in random.sample(walls, min(num_to_remove, len(walls))):
                self.carve_passage(a, b)

    def __repr__(self) -> str:
        return (
            f"MazeGrid(width={self.width}, height={self.height}, "
            f"edges={sum(len(v) for v in self.graph.values()) // 2})"
        )


def run_algorithm(config: Config) -> MazeGrid:
    if config.seed is not None:
        random.seed(config.seed)
    maze = MazeGrid(config.width, config.height, config.entry, config.exit)
    visited: Set[Cell] = maze.forty_two_logo(maze.width, maze.height)
    visited.add(config.entry)
    stack: List[Cell] = [config.entry]

    while stack:
        current = stack[-1]
        neighbor = maze.random_unvisited_neighbor(current, visited)
        if neighbor is None:
            stack.pop()
            continue

        maze.carve_passage(current, neighbor)
        visited.add(neighbor)
        stack.append(neighbor)

    if config.perfect is False:
        maze.make_imperfect(0.1)
    return maze


def get_maze(config_file: str) -> MazeGrid:
    try:
        config: Config = parse_config(config_file)
    except ConfigError as e:
        print(f"{e}")
        sys.exit(1)
    maze: MazeGrid = run_algorithm(config)
    return maze

# if __name__ == '__main__':
#     get_maze()