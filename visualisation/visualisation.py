import sys
from maze_generator.a_maze_ing import MazeGrid, MazeValidationError , run_algorithm
from parsing.parse_config import Config, parse_config, ConfigError

if __name__ == "__main__":
    try:
        config: Config = parse_config("config/config.txt")
    except ConfigError as e:
        print(f"{e}")
        sys.exit(1)

    maze: MazeGrid = run_algorithm(config)

    for cell in maze.graph:
        print(f"cell: {cell} value: {maze.graph[cell]}")