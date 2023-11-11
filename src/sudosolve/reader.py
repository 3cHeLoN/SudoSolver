"""Loader of sudoku files."""
import os
from dataclasses import dataclass

from colorama import Fore, Style


@dataclass
class Digit:
    """Represent a digit."""

    value: int
    fixed: bool = False

    def __repr__(self) -> str:
        if self.value == 0:
            return "   "
        str_value = ""
        if self.fixed:
            str_value += Fore.RED

        str_value += f" {self.value:d} "
        if self.fixed:
            str_value += Style.RESET_ALL

        return str_value


class SudoGrid:
    """Represent a sudoku grid."""

    def __init__(self, sudo_str: str) -> None:
        # TODO: add checks for valid str.
        self.fixed_digits = list(map(int, sudo_str.replace("_", "0")))
        self.digits = []

        for digit in self.fixed_digits:
            self.digits.append(Digit(digit, fixed=(digit != 0)))

    def show(self) -> None:
        """Print self."""
        print("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")
        for count, digit in enumerate(self.digits):
            column = count % 9
            row = count // 9
            if column % 3 == 0:
                print("║", end="")
            else:
                print("│", end="")
            print(digit, end="")

            if column == 8:
                print("║")
                if row == 8:
                    break
                if (row + 1) % 3 == 0:
                    print("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣")
                else:
                    print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")


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
