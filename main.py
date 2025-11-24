"""Batch simulation runner for Conway's Game of Life with snapshot logging.

This module provides functionality to run simulations without visualization,
saving the state of each generation to disk for later analysis or replay.
Useful for long-running simulations or batch processing of multiple patterns.
"""

from pathlib import Path
from datetime import datetime
from game_of_life.board import Board
from game_of_life.rules import evolve_grid
from game_of_life.errors import SimulationOverflowError, GameOfLifeError


def run_simulation(
    pattern_file: str,
    rows: int = 20,
    cols: int = 20,
    generations: int = 10,
    rule_name: str = "conway",
    log_dir: str = "logs",
):
    """Runs a headless Game of Life simulation with generation snapshots.

    Loads an initial pattern and evolves it for the specified number of
    generations, saving each state to a timestamped text file in the log
    directory. This enables batch processing and post-simulation analysis
    without real-time visualization overhead.

    Args:
        pattern_file: Path to text file containing the initial pattern.
        rows: Number of rows in the game board grid. Defaults to 20.
        cols: Number of columns in the game board grid. Defaults to 20.
        generations: Number of generations to simulate. Defaults to 10.
        rule_name: Rule set to apply (e.g., "conway"). Defaults to "conway".
        log_dir: Directory path where snapshots will be saved. Defaults to "logs".

    Raises:
        SimulationOverflowError: If generations exceeds 10,000 (safety limit).
        GameOfLifeError: If pattern loading or board operations fail.

    Note:
        Files are named with the pattern:
        {pattern_name}_{rule}_{generation}_{timestamp}.txt
        This allows multiple runs to coexist without overwriting.
    """
    if generations > 10_000:
        raise SimulationOverflowError(f"Too many generations: {generations}")

    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = Path(pattern_file).stem
    print(f"Starting simulation for pattern {base_name!r}, rule={rule_name}")

    for gen in range(generations + 1):
        snapshot_name = f"{base_name}_{rule_name}_gen{gen:04d}_{timestamp}.txt"
        board.save_snapshot(log_path / snapshot_name)

        if gen < generations:
            board.grid = evolve_grid(board.grid, rule_name)


if __name__ == "__main__":
    try:
        run_simulation(
            pattern_file="patterns/blinker.txt",
            rows=5,
            cols=5,
            generations=5,
            rule_name="conway",
        )
    except GameOfLifeError as e:
        print(f"[Error] {e}")