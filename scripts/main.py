import logging

from sudosolve.reader import SpfLoader


def main():
    loader = SpfLoader()
    sudokus = loader.load("sudokus.spf")
    for sudoku in sudokus:
        sudoku.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
