"""Visualization module for Conway's Game of Life using matplotlib animation.

This module provides animated visualization of Game of Life patterns, displaying
the evolution of cellular automata over multiple generations.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from game_of_life.board import Board
from game_of_life.rules import evolve_grid


def animate_game(pattern_file, rows=20, cols=20, generations=100):
    """Animates Conway's Game of Life simulation from a pattern file.

    Loads an initial pattern, evolves it according to Game of Life rules,
    and displays an animated visualization showing the progression through
    multiple generations. The animation updates every 200 milliseconds.

    Args:
        pattern_file: Path to text file containing the initial pattern.
        rows: Number of rows in the game board grid. Defaults to 20.
        cols: Number of columns in the game board grid. Defaults to 20.
        generations: Number of generations to simulate and display. Defaults to 100.
    """
    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    fig, ax = plt.subplots()
    ax.set_title("Conway's Game of Life Simulation")

    img = ax.imshow(board.grid, cmap="binary")

    def update(frame):
        """Updates the board state for each animation frame.

        Args:
            frame: Current frame number (generation count).

        Returns:
            List containing the updated image artist for blitting.
        """
        board.grid = evolve_grid(board.grid)
        img.set_data(board.grid)
        ax.set_xlabel(f"Generation: {frame}")
        return [img]

    ani = animation.FuncAnimation(
        fig, update, frames=generations, interval=200, blit=True
    )

    plt.show()


if __name__ == "__main__":
    animate_game("patterns/blinker.txt", rows=5, cols=5, generations=20)
