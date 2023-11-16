"""Loader of sudoku files."""
import itertools
import logging
import os

import numpy as np
from colorama import Fore, Style

import sudosolve.util
from sudosolve.util import coordinates_to_linear


class Digit:
    """Represent a digit."""

    def __init__(self, value: int, fixed: bool = False):
        self.value = value
        self.fixed = fixed

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
        digit_list = list(map(int, sudo_str.replace("_", "0")))
        self.bitmap = np.zeros((9, 9), dtype=int)
        self.possibles = ((1 << 9) - 1) * np.ones((9, 9), dtype=int)
        self.digits = [None] * 81
        self.sees = self._build_sees()

        for idx, value in enumerate(digit_list):
            # Initialize
            self.digits[idx] = Digit(0)
            row, col = sudosolve.util.linear_to_coordinates(idx)
            self.set(row, col, value, fixed=value != 0)

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

    def get_valid_digits(self, row: int, col: int) -> list[int]:
        cell_idx = row // 3 * 3 + col // 3
        pmask = (
            self.row_possibles[row]
            & self.col_possibles[col]
            & self.cell_possibles[cell_idx]
        )
        digits = []
        for idx in range(1, 10):
            if pmask & (1 << (idx - 1)):
                digits.append(idx)
        return digits

    def set(self, row: int, col: int, value: int, fixed: bool = False) -> None:
        idx = row * 9 + col

        if self.digits[idx].fixed:
            raise ValueError("Cannot overwrite a fixed digit.")

        if fixed:
            self.digits[idx].fixed = True

        self.digits[idx].value = value
        if value == 0:
            self.bitmap[row, col] = 0
        else:
            self.bitmap[row, col] = 1 << (value - 1)

        self.set_possibles()

    def check_valid(self) -> bool:
        """Check if no double digits."""
        # Check rows.
        rows_valid = self._check_valid_axis(axis=1)
        cols_valid = self._check_valid_axis(axis=0)
        valid_boxes = [self._check_box_valid(box_index) for box_index in range(9)]

        return rows_valid & cols_valid & all(valid_boxes)

    def set_possibles(self) -> None:
        """Check possible candidates in the grid."""
        all_possible = (1 << 9) - 1
        self.row_possibles = all_possible ^ np.bitwise_or.reduce(self.bitmap, axis=0)
        self.col_possibles = all_possible ^ np.bitwise_or.reduce(self.bitmap, axis=1)
        self.cell_possibles = np.zeros((9,), dtype=int)
        for cell_idx in range(9):
            box_row = cell_idx // 3
            box_col = cell_idx % 3

            box_slice = (
                slice(box_row * 3, box_row * 3 + 3),
                slice(box_col * 3, box_col * 3 + 3),
            )
            box_values = self.bitmap[box_slice].ravel()
            self.cell_possibles[cell_idx] = all_possible ^ np.bitwise_xor.reduce(
                box_values
            )

        # self.possibles = np.ones((9, 9), dtype=int) * ((1 << 9) - 1)
        # candidates_r = self.possibles.ravel()
        # bitmap_r = self.bitmap.ravel()
        # for idx in range(81):
        #     for see_index in self.sees[idx]:
        #         candidates_r[idx] &= ~bitmap_r[see_index]

    def _build_sees(self) -> list[Digit]:
        """Check what digits it sees."""
        sees = {}
        for idx in range(81):
            row, col = sudosolve.util.linear_to_coordinates(idx)
            col_coordinates = [(row_coor, col) for row_coor in range(9)]
            row_coordinates = [(row, col_coor) for col_coor in range(9)]
            cell_coordinates = [
                (row_coor, col_coor)
                for row_coor in range(row // 3, row // 3 + 3)
                for col_coor in range(col // 3, col // 3 + 3)
            ]
            linear_indices = [
                sudosolve.util.coordinates_to_linear(row_coor, col_coor)
                for row_coor, col_coor in col_coordinates
                + row_coordinates
                + cell_coordinates
            ]
            sees[idx] = linear_indices
        return sees

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
