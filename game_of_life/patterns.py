
import re
from pathlib import Path
from game_of_life.errors import PatternParseError

# Regex for lines like: (1,2) *  or (0, 4) .
COORD_LINE_RE = re.compile(
    r"^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s+([*.])\s*$"
)

def parse_pattern_file(path: Path):
    """
    Parse a pattern description file into a list of live-cell coordinates.

    Returns:
        rows, cols, live_cells
        where live_cells is a list of (row, col) tuples.
    """
    if not path.exists():
        raise PatternParseError(f"Pattern file not found: {path}")

    live_cells = []
    max_row = 0
    max_col = 0

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Ignore comments/blank lines

            m = COORD_LINE_RE.match(line)
            if not m:
                raise PatternParseError(
                    f"Malformed line {line_no} in {path}: {line!r}"
                )

            row = int(m.group(1))
            col = int(m.group(2))
            symbol = m.group(3)
            if symbol == "*":
                live_cells.append((row, col))
                max_row = max(max_row, row)
                max_col = max(max_col, col)

    # Infer grid size from max coordinates (inclusive)
    rows = max_row + 1
    cols = max_col + 1
    return rows, cols, live_cells
