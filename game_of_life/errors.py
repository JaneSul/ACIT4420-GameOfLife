

class GameOfLifeError(Exception):
    """Base class for Game of Life domain errors."""
    pass


class GridSizeError(GameOfLifeError):
    """Raised when grid dimensions are invalid."""
    pass


class PatternParseError(GameOfLifeError):
    """Raised when pattern files have invalid or malformed content."""
    pass


class SimulationOverflowError(GameOfLifeError):
    """Raised when simulation tries to run for too many generations."""
    pass
