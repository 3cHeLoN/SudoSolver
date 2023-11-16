from unittest import TestCase

from sudosolve.reader import SudoGrid, Digit


class TestSudoGrid(TestCase):
    def setUp(self):
        self.empty = SudoGrid()

    def test_check_valid(self):
        self.assertTrue(self.empty.check_valid())

    def test_wrong_row(self):
        wrong_row = SudoGrid()
        wrong_row.set(row=0, col=0, digit=Digit(1))
        wrong_row.set(row=0, col=2, digit=Digit(1))
        self.assertFalse(wrong_row.check_valid())
        self.assertTrue(wrong_row._check_valid_axis(axis=0))

    def test_wrong_col(self):
        wrong_col = SudoGrid()
        wrong_col.set(row=0, col=4, digit=Digit(2))
        wrong_col.set(row=6, col=4, digit=Digit(2))
        wrong_col.set(row=3, col=4, digit=Digit(3))
        self.assertFalse(wrong_col.check_valid())
        self.assertTrue(wrong_col._check_valid_axis(axis=1))

    def test_wrong_cell(self):
        wrong_cell = SudoGrid()
        wrong_cell.set(row=0, col=0, digit=Digit(5))
        wrong_cell.set(row=2, col=2, digit=Digit(5))
        self.assertFalse(wrong_cell.check_valid())

    def test_correct_cells(self):
        correct_cell = SudoGrid()
        correct_cell.set(row=0, col=0, digit=Digit(7))
        correct_cell.set(row=3, col=3, digit=Digit(7))
        self.assertTrue(correct_cell.check_valid())
