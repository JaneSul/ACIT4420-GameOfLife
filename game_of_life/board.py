# grid management and file handling
from pathlib import Path
from game_of_life.errors import GridSizeError
from game_of_life.patterns import parse_pattern_file


class Board:
    """Represents the Game of Life grid."""

    def __init__(self, rows: int, cols: int):
        if rows <= 0 or cols <= 0:
            raise GridSizeError(f"Invalid grid size: {rows}x{cols}")
        self.rows = rows
        self.cols = cols
        # 0 = dead, 1 = alive
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def load_pattern(self, pattern_path: str):
        """
        Load initial live cells from a pattern file into the existing grid.

        If the pattern is bigger than the current grid, this method
        raises GridSizeError instead of silently truncating.
        """
        path = Path(pattern_path)
        rows, cols, live_cells = parse_pattern_file(path)

        if rows > self.rows or cols > self.cols:
            raise GridSizeError(
                f"Pattern ({rows}x{cols}) does not fit into board {self.rows}x{self.cols}"
            )

        # Clear grid then place live cells
        self.clear()
        for r, c in live_cells:
            self.grid[r][c] = 1

    def clear(self):
        """Set all cells to dead."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = 0

    def save_snapshot(self, out_path: str):
        """
        Save current grid state to a text file (for logging/debugging).
        """
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Simple ASCII format: '.' for dead, '*' for alive
        with path.open("w", encoding="utf-8") as f:
            for row in self.grid:
                line = "".join("*" if cell == 1 else "." for cell in row)
                f.write(line + "\n")
