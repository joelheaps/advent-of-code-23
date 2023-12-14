from .solve import shift_rocks_in_line

def test_shift_rocks_in_line():
    line = "..O."
    assert shift_rocks_in_line(line) == "O..."

    line = "..#..O."
    assert shift_rocks_in_line(line) == '..#O...'

    line = "#..O..O"
    assert shift_rocks_in_line(line) == '#OO....'
