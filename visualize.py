# visualize.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from game_of_life.board import Board
from game_of_life.rules import evolve_grid


def animate_game(pattern_file, rows=20, cols=20, generations=100):
    # Load board
    board = Board(rows, cols)
    board.load_pattern(pattern_file)

    fig, ax = plt.subplots()
    ax.set_title("Conway's Game of Life Simulation")

    # Create image handle
    img = ax.imshow(board.grid, cmap='binary')

    def update(frame):
        board.grid = evolve_grid(board.grid)
        img.set_data(board.grid)
        ax.set_xlabel(f"Generation: {frame}")
        return [img]

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=generations,
        interval=200,  # milliseconds per frame
        blit=True
    )

    plt.show()


if __name__ == "__main__":
    animate_game("patterns/blinker.txt", rows=5, cols=5, generations=20)
