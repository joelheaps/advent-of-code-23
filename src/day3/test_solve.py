from .solve import is_valid_part_loc, symbol_adjacent, get_number_locations
import pytest


@pytest.fixture
def test_string() -> str:
    return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test_symbol_adjacent(test_string):
    lines = test_string.splitlines()
    assert not symbol_adjacent(lines[0], first=0, last=2)
    assert symbol_adjacent(lines[1], first=1, last=2)


def test_is_valid_part_loc(test_string):
    # Check if substring is part number
    assert is_valid_part_loc(test_string, line_n=0, first=0, last=2)
    assert not is_valid_part_loc(test_string, line_n=0, first=5, last=7)


def test_get_number_locations(test_string):
    number_location_tuples: list[tuple[int, int, int, int]] = get_number_locations(
        test_string
    )

    assert (467, 0, 0, 2) in number_location_tuples
    assert (664, 9, 1, 3) in number_location_tuples
