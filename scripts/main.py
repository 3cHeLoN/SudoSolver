from sudosolve.reader import SpfLoader


def main():
    loader = SpfLoader("sudokus.spf")
    sudokus = loader.load()
    for sudoku in sudokus:
        sudoku.show()


if __name__ == "__main__":
    main()
