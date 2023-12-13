import pytest
from .solve import (
    mirror_left_side,
    check_row_symmetry_at_column,
    check_all_rows_for_symmetry_at_column,
    find_symmetry_column,
)


@pytest.fixture
def vertical_pattern() -> str:
    return """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#."""


def test_mirror_left_side():
    assert mirror_left_side("asdf", 2) == "sa"
    assert mirror_left_side("012345", 4) == "3210"
    assert mirror_left_side("asdf", 0) == ""


def test_check_row_symmetry_at_column():
    assert check_row_symmetry_at_column("01233210", 4)
    assert not check_row_symmetry_at_column("0123210", 4)
    assert not check_row_symmetry_at_column("0123", 0)


def test_check_all_rows_for_symmetry_at_column(vertical_pattern):
    assert check_all_rows_for_symmetry_at_column(vertical_pattern, 5)
    assert not check_all_rows_for_symmetry_at_column(vertical_pattern, 2)


def test_find_symmetry_column(vertical_pattern):
    assert find_symmetry_column(vertical_pattern) == 5
    assert find_symmetry_column("9678dfv") is None
