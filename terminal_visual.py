"""Console-based simulation runner for Conway's Game of Life.

This module provides a text-based visualization of Game of Life patterns
in the terminal, using block characters to represent live cells and clearing
the screen between generations for animation effect.
"""

import time
import os
from game_of_life.board import Board
from game_of_life.rules import evolve_grid


def print_grid(grid):
    """Prints the game board to the console using block characters.

    Live cells are displayed as filled blocks (█) and dead cells as spaces,
    creating a visual representation of the current board state.

    Args:
        grid: 2D list representing the game board where True indicates
            a live cell and False indicates a dead cell.
    """
    for row in grid:
        print("".join("█" if cell else " " for cell in row))


def run(pattern_file, rows=20, cols=20, generations=100):
    """Runs a console-based Game of Life simulation with terminal clearing.

    Loads an initial pattern and simulates its evolution over multiple
    generations. The terminal is cleared before each generation is displayed,
    creating an animated effect. Each frame is displayed for 0.2 seconds.

    Args:
        pattern_file: Path to text file containing the initial pattern.
        rows: Number of rows in the game board grid. Defaults to 20.
        cols: Number of columns in the game board grid. Defaults to 20.
        generations: Number of generations to simulate. Defaults to 100.

    """
    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    for gen in range(generations):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Generation {gen}")
        print_grid(board.grid)
        board.grid = evolve_grid(board.grid)
        time.sleep(0.2)


if __name__ == "__main__":
    run("patterns/blinker.txt", 5, 5, 20)