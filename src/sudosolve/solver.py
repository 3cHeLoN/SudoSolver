"""The solver code."""
from sudosolve.reader import SudoGrid


class Solver:
    """The solver class."""

    def solve(self, grid: SudoGrid) -> SudoGrid:
        """Solve the grid.

        Args:
            grid: The Sudoku grid to solve.

        Returns:
            The solved grid.
        """
        solved = False

        while not solved:
            pass

    def _check_digit(self, idx: int) -> bool:
        """Check if the filled in digit is valid."""
