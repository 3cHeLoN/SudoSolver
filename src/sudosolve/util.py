"""Utilities."""


def linear_to_coordinates(index: int) -> tuple[int, int]:
    """Return row and column indices."""
    return index // 9, index % 9


def coordinates_to_linear(row: int, col: int) -> int:
    return row * 9 + col
