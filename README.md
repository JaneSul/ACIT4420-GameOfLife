# Conway's Game of Life

A Python implementation of Conway's Game of Life cellular automaton.

The system simulates the evolution of cellular patterns based on:

- Birth rules (dead cells with exactly 3 neighbors become alive)
- Survival rules (live cells with 2-3 neighbors survive)
- Death rules (cells die from underpopulation or overcrowding)

It validates grid configurations, processes cell states through generations, supports multiple initial patterns, logs simulation steps, and outputs structured results.

This project demonstrates:

- Modular Python package design
- Classes, functions, decorators (metaprogramming)
- File I/O (pattern loading/saving)
- Logging & performance timing
- CLI interface
- Automated testing with pytest

## Installation
Clone the repository
```shell
git clone https://github.com/JaneSul/ConwaysGameOfLife.git
cd ConwaysGameOfLife
```
Alternatively, create a virtualenv
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Running the Program
Run the program with any of
```shell
python teminal_visual_blink.py
python terminal_visual.py
python visualize.py

```

This will start the simulations!
