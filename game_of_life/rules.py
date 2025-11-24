# evolutionary logic and metaprogramming rule registry
from typing import Callable, Dict, List

RuleFunc = Callable[[int, int], int]  # (current_state, live_neighbors) -> new_state

_RULES_REGISTRY: Dict[str, RuleFunc] = {}


def register_rule(name: str):
    """
    Decorator that registers a rule function in the global registry.

    Usage:
        @register_rule("conway")
        def conway_rule(state, neighbors): ...
    """
    def decorator(func: RuleFunc) -> RuleFunc:
        _RULES_REGISTRY[name] = func
        return func
    return decorator


def get_rule(name: str) -> RuleFunc:
    try:
        return _RULES_REGISTRY[name]
    except KeyError:
        raise ValueError(f"Unknown rule set: {name}. Registered: {list(_RULES_REGISTRY)}")


@register_rule("conway")
def conway_rule(current_state: int, live_neighbors: int) -> int:
    """
    Classic Conway Game of Life rule (B3/S23).
    """
    if current_state == 1:
        # Survival with 2 or 3 neighbors
        return 1 if live_neighbors in (2, 3) else 0
    else:
        # Birth with exactly 3 neighbors
        return 1 if live_neighbors == 3 else 0


def count_live_neighbors(grid: List[List[int]], r: int, c: int) -> int:
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
    """
    Compute the next generation of the grid using the selected rule.
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
