"""Optimized console-based simulation runner for Conway's Game of Life.

This module provides an efficient text-based visualization using ANSI escape
codes to redraw frames in place without clearing the screen, resulting in
smoother animation with reduced flickering.
"""

import time
from game_of_life.board import Board
from game_of_life.rules import evolve_grid


def print_grid(grid):
    """Converts the game board into a formatted string for rendering.

    Creates a multi-line string representation of the grid using block
    characters for live cells and spaces for dead cells. This pre-formatting
    approach improves rendering performance.

    Args:
        grid: 2D list representing the game board where True indicates
            a live cell and False indicates a dead cell.

    Returns:
        Multi-line string representation of the grid ready for display.
    """
    return "\n".join("".join("█" if cell else " " for cell in row) for row in grid)


def run(pattern_file, rows=20, cols=20, generations=200, delay=0.1):
    """Runs an optimized console-based Game of Life simulation.

    Loads an initial pattern and simulates its evolution using ANSI escape
    codes to redraw frames in place. The cursor is moved up to overwrite
    previous frames, creating smooth animation without screen flickering.
    The cursor is hidden during simulation for cleaner display.

    Args:
        pattern_file: Path to text file containing the initial pattern.
        rows: Number of rows in the game board grid. Defaults to 20.
        cols: Number of columns in the game board grid. Defaults to 20.
        generations: Number of generations to simulate. Defaults to 200.
        delay: Time delay between frames in seconds. Defaults to 0.1.

    Example:
        >>> run("patterns/glider.txt", rows=10, cols=10, generations=100, delay=0.05)

    Note:
        This implementation uses ANSI escape codes which work on most modern
        terminals but may not be compatible with older Windows command prompts.
    """
    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    print("\033[?25l", end="")

    try:
        first_frame = True
        for gen in range(generations):

            grid_str = print_grid(board.grid)

            if first_frame:
                print(f"Generation {gen}")
                print(grid_str)
                first_frame = False
            else:
                lines_to_move = rows + 1
                print(f"\033[{lines_to_move}A", end="")

                print(f"Generation {gen}")
                print(grid_str)

            board.grid = evolve_grid(board.grid)
            time.sleep(delay)

    finally:
        print("\033[?25h", end="")
