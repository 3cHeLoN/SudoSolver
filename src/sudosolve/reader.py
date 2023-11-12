"""Loader of sudoku files."""
import logging
import os
from dataclasses import dataclass

import numpy as np
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

    def __init__(self, sudo_str: str = "0" * 81) -> None:
        # TODO: add checks for valid str.
        self.fixed_digits = list(map(int, sudo_str.replace("_", "0")))
        self.bitmap = np.zeros((9, 9), dtype=int)
        self.digits = []

        for count, digit in enumerate(self.fixed_digits):
            row = count // 9
            col = count % 9
            self.digits.append(Digit(digit, fixed=digit != 0))
            if digit == 0:
                continue
            self.bitmap[row, col] = 1 << (digit - 1)

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

    def get(self, row: int, col: int) -> int:
        """Get the value."""
        idx = row * 9 + col
        return self.digits[idx].value

    def get_digit(self, row: int, col: int) -> Digit:
        """Return a digit."""
        idx = row * 9 + col
        return self.digits[idx]

    def set(self, row: int, col: int, value: int) -> None:
        idx = row * 9 + col
        if self.digits[idx].fixed:
            raise ValueError("The digit is fixed.")

        self.digits[idx] = Digit(value)

        if value == 0:
            self.bitmap[row, col] = 0
        else:
            self.bitmap[row, col] = 1 << (value - 1)

    def check_valid(self) -> bool:
        """Check if no double digits."""
        # Check rows.
        rows_valid = self._check_valid_axis(axis=1)
        cols_valid = self._check_valid_axis(axis=0)
        valid_boxes = [self._check_box_valid(box_index) for box_index in range(9)]

        return rows_valid & cols_valid & all(valid_boxes)

    def _check_box_valid(self, box_index: int) -> bool:
        box_row = box_index // 3
        box_col = box_index % 3

        box_slice = (
            slice(box_row * 3, box_row * 3 + 3),
            slice(box_col * 3, box_col * 3 + 3),
        )
        box_values = self.bitmap[box_slice].ravel()
        value_check = np.bitwise_xor.reduce(box_values)
        occupancy_check = np.bitwise_or.reduce(box_values)
        return (value_check & occupancy_check == occupancy_check).all()

    def _check_valid_axis(self, axis) -> bool:
        value_check = np.bitwise_xor.reduce(self.bitmap, axis=axis)
        occupancy_check = np.bitwise_or.reduce(self.bitmap, axis=axis)
        return (value_check & occupancy_check == occupancy_check).all()


class SpfLoader:
    """Loads spf files."""

    def load(self, filename: str | bytes | os.PathLike):
        with open(filename, encoding="utf-8") as handle:
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
            logging.warning("The file does not have a valid header.")

        # Remove header text.
        sudokus = text.splitlines()[1:]

        grids = []
        for sudoku in sudokus:
            grids.append(SudoGrid(sudoku))

        return grids
