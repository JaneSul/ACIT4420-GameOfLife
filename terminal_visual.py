
import time
import os
from game_of_life.board import Board
from game_of_life.rules import evolve_grid

def print_grid(grid):
    for row in grid:
        print("".join("█" if cell else " " for cell in row))

def run(pattern_file, rows=20, cols=20, generations=100):
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
