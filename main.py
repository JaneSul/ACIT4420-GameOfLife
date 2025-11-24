
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
    """
    Run a simulation from a pattern file for a fixed number of generations,
    saving snapshots to disk.
    """
    if generations > 10_000:
        # Example safeguard
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
    # Simple CLI interface; could be extended with argparse
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
