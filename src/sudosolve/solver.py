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
        self.grid = grid
        solved = False
        self.count = 0

        while not solved:
            self._check_digit(0)

    def _check_digit(self, idx: int) -> bool:
        """Check if the filled in digit is valid."""
        self.count += 1
        if self.count % 1000 == 0:
            self.grid.show()
        if idx > 80:
            return False

        row = idx // 9
        col = idx % 9
        digit = self.grid.get_digit(row, col)
        if digit.fixed:
            self._check_digit(idx + 1)
            return False

        value = digit.value
        while value < 9:
            self.grid.set(row, col, value + 1)
            if self.grid.check_valid():
                self._check_digit(idx + 1)
            value += 1

        # All digits failed?
        self.grid.set(row, col, 0)
        return False
