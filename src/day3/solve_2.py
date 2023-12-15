import re
from reader import input_data

# Get unique symbols from input data
INPUT_LINES = input_data.splitlines()


def get_full_number(s: str, col: int) -> int:
    """Given location of a part of a number, gets full number."""
    for match in re.finditer(r"\d+", s):
        if col in range(match.start(), match.end()):
            return int(match.group())


def get_neighbor_numbers(pattern: str, row: int, col: int) -> tuple:
    neighbors: set[int] = set()
    # Check adjacent cells for numbers
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            try:
                if pattern[r][c].isdigit():
                    neighbors.add(get_full_number(pattern[r], c))
            except IndexError:
                pass
    return tuple(neighbors)


def get_gears():
    possible_gears = []

    for r, line in enumerate(INPUT_LINES):
        for match in re.finditer(r"\*", line):
            possible_gears.append(get_neighbor_numbers(INPUT_LINES, r, match.start()))

    gears = [gear for gear in possible_gears if len(gear) == 2]

    return gears


gears = get_gears()
print("Gears:", gears)

sum_of_ratios: int = sum([first_r * last_r for first_r, last_r in gears])

print("Sum of ratios:", sum_of_ratios)
