from .solve import (
    shift_rocks_in_line,
    slide_rocks_north,
    slide_rocks_west,
    slide_rocks_south,
)


def test_shift_rocks_in_line():
    line = "..O."
    assert shift_rocks_in_line(line) == "O..."

    line = "..#..O."
    assert shift_rocks_in_line(line) == "..#O..."

    line = "#..O..O"
    assert shift_rocks_in_line(line) == "#OO...."


def test_slide_rocks_north():
    pattern = """..
..
OO"""

    assert (
        slide_rocks_north(pattern)
        == """OO
..
.."""
    )


def test_slide_rocks_west():
    pattern = """.O.
#.O"""

    assert (
        slide_rocks_west(pattern)
        == """O..
#O."""
    )


def test_slide_rocks_south():
    pattern = """OO
..
#."""

    assert (
        slide_rocks_south(pattern)
        == """..
O.
#O"""
    )
