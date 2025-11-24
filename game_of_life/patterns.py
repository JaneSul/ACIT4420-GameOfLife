"""Pattern file parsing utilities for Game of Life initial configurations.

This module handles parsing of pattern description files that specify initial
cell positions using coordinate notation.
"""

import re
from pathlib import Path
from game_of_life.errors import PatternParseError


COORD_LINE_RE = re.compile(r"^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s+([*.])\s*$")
"""Regex pattern for coordinate lines in format: (row, col) symbol

Matches lines like "(1, 2) *" or "(0,4) ." with flexible whitespace.
Captures three groups: row number, column number, and cell symbol (* or .).
"""


def parse_pattern_file(path: Path):
    """Parses a pattern description file into live cell coordinates.

    Reads a text file where each line specifies a cell coordinate and state
    using the format "(row, col) symbol". Lines starting with '#' are treated
    as comments and blank lines are ignored. Live cells are marked with '*'
    and dead cells with '.'.

    The grid dimensions are automatically inferred from the maximum row and
    column values found in the file.

    Args:
        path: Path object pointing to the pattern file to parse.

    Returns:
        A tuple of (rows, cols, live_cells) where:
            - rows (int): Inferred grid height (max_row + 1)
            - cols (int): Inferred grid width (max_col + 1)
            - live_cells (list): List of (row, col) tuples for live cells

    Raises:
        PatternParseError: If the file doesn't exist or contains malformed lines.

    Note:
        Pattern file format:
            # Comment lines start with #
            (0, 1) *  # Live cell at row 0, col 1
            (1, 0) .  # Dead cell (optional, can be omitted)
            (1, 1) *  # Live cell at row 1, col 1
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
                continue

            m = COORD_LINE_RE.match(line)
            if not m:
                raise PatternParseError(f"Malformed line {line_no} in {path}: {line!r}")

            row = int(m.group(1))
            col = int(m.group(2))
            symbol = m.group(3)
            if symbol == "*":
                live_cells.append((row, col))
                max_row = max(max_row, row)
                max_col = max(max_col, col)

    rows = max_row + 1
    cols = max_col + 1
    return rows, cols, live_cells
