# pytest test implementing the assigned test

import pytest
from game_of_life.board import Board
from game_of_life.rules import evolve_grid


def test_load_pattern():
    board = Board(5, 5)
    board.load_pattern("patterns/test_pattern.txt")
    assert board.grid[0][0] == 1


def test_evolve_grid():
    grid = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    new_grid = evolve_grid(grid)
    assert new_grid[1][1] == 1  # Blinker persists


def test_board_init():
    board = Board(10, 10)
    assert len(board.grid) == 10
    assert all(all(cell == 0 for cell in row) for row in board.grid)
