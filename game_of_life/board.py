"""Grid management and file handling for Game of Life board state.

This module provides the Board class for managing the game grid, including
initialization, pattern loading, state persistence, and grid manipulation.
"""

from pathlib import Path
from game_of_life.errors import GridSizeError
from game_of_life.patterns import parse_pattern_file


class Board:
    """Represents the Game of Life grid with pattern loading and persistence.

    The board maintains a 2D grid where each cell can be either alive (1) or
    dead (0). Provides methods for loading patterns from files, clearing the
    grid, and saving snapshots for analysis or debugging.

    Attributes:
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        grid: 2D list representing cell states (0=dead, 1=alive).
    """

    def __init__(self, rows: int, cols: int):
        """Initializes a new game board with the specified dimensions.

        Creates a grid filled with dead cells (zeros). The grid can later
        be populated using load_pattern or by directly modifying the grid.

        Args:
            rows: Number of rows in the grid (must be positive).
            cols: Number of columns in the grid (must be positive).

        Raises:
            GridSizeError: If rows or cols is less than or equal to zero.
        """
        if rows <= 0 or cols <= 0:
            raise GridSizeError(f"Invalid grid size: {rows}x{cols}")
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def load_pattern(self, pattern_path: str):
        """Loads an initial pattern from a file into the grid.

        Parses the pattern file and places live cells at their specified
        coordinates. The grid is cleared before loading. If the pattern
        dimensions exceed the board size, an error is raised to prevent
        truncation.

        Args:
            pattern_path: Path to the pattern file to load.

        Raises:
            GridSizeError: If the pattern dimensions exceed the board size.
            FileNotFoundError: If the pattern file does not exist.
            ValueError: If the pattern file format is invalid.
        """
        path = Path(pattern_path)
        rows, cols, live_cells = parse_pattern_file(path)

        if rows > self.rows or cols > self.cols:
            raise GridSizeError(
                f"Pattern ({rows}x{cols}) does not fit into board {self.rows}x{self.cols}"
            )

        self.clear()
        for r, c in live_cells:
            self.grid[r][c] = 1

    def clear(self):
        """Resets all cells in the grid to dead state.

        Sets every cell in the grid to 0 (dead), effectively clearing
        the board for a fresh pattern or simulation.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = 0

    def save_snapshot(self, out_path: str):
        """Saves the current grid state to a text file.

        Writes the grid in ASCII format where '*' represents alive cells
        and '.' represents dead cells. Creates parent directories if they
        don't exist. Useful for logging, debugging, or creating pattern files.

        Args:
            out_path: Path where the snapshot file will be saved.

        Note:
            Output format uses '.' for dead cells and '*' for alive cells,
            one row per line.
        """
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            for row in self.grid:
                line = "".join("*" if cell == 1 else "." for cell in row)
                f.write(line + "\n")