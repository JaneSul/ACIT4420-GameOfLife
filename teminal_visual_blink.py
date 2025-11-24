import time
import sys
from game_of_life.board import Board
from game_of_life.rules import evolve_grid

def print_grid(grid):
    """Convert grid into a string for fast rendering."""
    return "\n".join("".join("█" if cell else " " for cell in row) for row in grid)

def run(pattern_file, rows=20, cols=20, generations=200, delay=0.1):
    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    # Prepare screen once
    print("\033[?25l", end="")   # Hide cursor

    try:
        first_frame = True
        for gen in range(generations):

            grid_str = print_grid(board.grid)

            if first_frame:
                # First print: output everything normally
                print(f"Generation {gen}")
                print(grid_str)
                first_frame = False
            else:
                # ANSI code: Move cursor up (#rows + 1) lines
                lines_to_move = rows + 1
                print(f"\033[{lines_to_move}A", end="")

                # Rewrite frame in place
                print(f"Generation {gen}")
                print(grid_str)

            board.grid = evolve_grid(board.grid)
            time.sleep(delay)

    finally:
        print("\033[?25h", end="")  # Show cursor again
