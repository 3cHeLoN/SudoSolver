"""The solver code."""
from time import time

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
        self.grid = grid
        solved = False
        self.count = 0
        self.t_start = time()

        while not solved:
            self._check_digit(0)

    def _check_candidates(self) -> None:
        """Check candidates."""
        pass

    def _check_digit(self, idx: int) -> bool:
        """Check if the filled in digit is valid."""
        self.count += 1
        if self.count % 1000 == 0:
            print(self.count / (time() - self.t_start), "per second")
            self.grid.show()

        if idx > 80:
            return False

        row = idx // 9
        col = idx % 9
        digit = self.grid.get_digit(row, col)
        valid_digits = self.grid.get_valid_digits(row, col)

        if digit is not None and digit.fixed:
            self._check_digit(idx + 1)
            return False

        for value in valid_digits:
            self.grid.set(row, col, value)
            if self.grid.check_valid():
                self._check_digit(idx + 1)
            value += 1

        # All digits failed?
        self.grid.set(row, col, 0)
        return False
