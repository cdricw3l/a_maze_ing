from amazing.maze_generator.a_maze_ing import MazeGrid

def visualisation_maze(maze: MazeGrid) -> None:
    for cell in maze.graph:
        print(f"cell: {cell} value: {maze.graph[cell]}")
