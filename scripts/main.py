"""Start the solver."""
import logging

from sudosolve.reader import SpfLoader
from sudosolve.solver import Solver


def main():
    loader = SpfLoader()
    sudokus = loader.load(filename="sudokus.spf")
    for sudoku in sudokus:
        sudoku.show()

    solver = Solver()
    solver.solve(sudokus[0])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
