"""Loader of sudoku files."""


import os
import numpy as np


class SudoGrid:
    def __init__(self, sudo_str: str) -> None:
        # TODO: add checks for valid str.
        self.fixed_digits = np.array(sudo_str.replace("_", "0"), dtype=int).reshape(
            (9, 9)
        )
        self.digits = self.fixed_digits.copy()

    def show(self) -> None:
        """Print self."""
        for count, digit in enumerate(self.digits):
            if count % 9 == 0:
                print("\n")
            if digit == 0:
                print(" ", end=false)

            print(digit, end=false)


class SpfLoader:
    """Loads spf files."""

    def __init__(self, filename: str | bytes | os.PathLike):
        self.filename = filename

    def load(self):
        with open(self.filename, encoding="utf-8") as handle:
            text = handle.read()
        return self.loads(text)

    def loads(self, text: str) -> list[SudoGrid]:
        """Interpret the spf text.

        Args:
            text (str): The input text.

        Returns:
            SudoGrid: The datastructure representing the sudoku.
        """
        text = text.lower()
        # Interpret the string.
        if not text.startswith("#spf1.0"):
            logging.warn("The file does not have a valid header.")

        # Remove header text.
        sudokus = text.splitlines()[1:]

        grids = []
        for sudoku in sudokus:
            grids.append(SudoGrid(sudoku))

        return grids
