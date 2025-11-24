"""Evolutionary logic and metaprogramming rule registry for Game of Life.

This module implements the core cellular automaton evolution logic with a
flexible rule registry system. Rules can be registered dynamically using
decorators, allowing for easy extension with custom rule sets beyond
Conway's classic rules.
"""

from typing import Callable, Dict, List

RuleFunc = Callable[[int, int], int]
"""Type alias for rule functions.

A rule function takes (current_state, live_neighbors) and returns the new
state (0 or 1) for a cell.
"""

_RULES_REGISTRY: Dict[str, RuleFunc] = {}
"""Global registry mapping rule names to their implementation functions."""


def register_rule(name: str):
    """Decorator that registers a rule function in the global registry.

    Allows custom rules to be registered by name for use with evolve_grid.
    The decorated function should implement the cellular automaton logic
    for determining cell state transitions.

    Args:
        name: Unique identifier for the rule set (e.g., "conway", "highlife").

    Returns:
        Decorator function that registers and returns the rule function unchanged.

    """
    def decorator(func: RuleFunc) -> RuleFunc:
        _RULES_REGISTRY[name] = func
        return func
    return decorator


def get_rule(name: str) -> RuleFunc:
    """Retrieves a registered rule function by name.

    Args:
        name: Name of the rule set to retrieve.

    Returns:
        The rule function associated with the given name.

    Raises:
        ValueError: If the rule name is not registered, includes list of
            available rules in the error message.
    """
    try:
        return _RULES_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown rule set: {name}. Registered: {list(_RULES_REGISTRY)}")


@register_rule("conway")
def conway_rule(current_state: int, live_neighbors: int) -> int:
    """Implements classic Conway's Game of Life rules (B3/S23).

    Standard cellular automaton rules:
    - Birth (B3): Dead cell with exactly 3 neighbors becomes alive
    - Survival (S23): Live cell with 2 or 3 neighbors stays alive
    - Death: All other cases result in dead cells

    Args:
        current_state: Current cell state (0=dead, 1=alive).
        live_neighbors: Count of live cells in the 8-cell neighborhood.

    Returns:
        New cell state (0=dead, 1=alive) for the next generation.
    """
    if current_state == 1:
        return 1 if live_neighbors in (2, 3) else 0
    else:
        return 1 if live_neighbors == 3 else 0


def count_live_neighbors(grid: List[List[int]], r: int, c: int) -> int:
    """Counts the number of live cells in the 8-cell Moore neighborhood.

    Examines all eight adjacent cells (horizontally, vertically, and
    diagonally) and counts how many are alive. Handles edge cases by
    only counting cells within grid boundaries.

    Args:
        grid: 2D list representing the current game state.
        r: Row index of the cell to check.
        c: Column index of the cell to check.

    Returns:
        Number of live neighbors (0-8).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                total += grid[nr][nc]
    return total


def evolve_grid(grid: List[List[int]], rule_name: str = "conway") -> List[List[int]]:
    """Computes the next generation of the grid using the specified rule.

    Applies the selected cellular automaton rule to every cell simultaneously,
    creating a new grid representing the next time step. The original grid
    is not modified.

    Args:
        grid: 2D list representing the current generation (0=dead, 1=alive).
        rule_name: Name of the registered rule to apply. Defaults to "conway".

    Returns:
        New 2D list representing the next generation with the same dimensions.

    Raises:
        ValueError: If the specified rule_name is not registered.

    """
    rule = get_rule(rule_name)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            neighbors = count_live_neighbors(grid, r, c)
            new_grid[r][c] = rule(grid[r][c], neighbors)

    return new_grid
