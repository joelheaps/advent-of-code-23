import re
from reader import input_data

# Get unique symbols from input data
SYMBOLS = set(filter(lambda char: not char.isdigit() and char not in "\n.", input_data))
INPUT_LINES = input_data.splitlines()


def is_adjacent_to_symbol(pattern: str, row: int, col: int) -> bool:
    # Check adjacent cells for symbols
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            try:
                if pattern[r][c] in SYMBOLS:
                    return True
            except IndexError:
                pass
    return False


def get_part_numbers():
    part_numbers = []

    for r, line in enumerate(INPUT_LINES):
        for match in re.finditer(r"\d+", line):
            number = match.group()
            possible_adjacencies = [
                is_adjacent_to_symbol(INPUT_LINES, r, c)
                for c in range(match.start(), match.end())
            ]
            if any(possible_adjacencies):
                part_numbers.append(int(number))

    return part_numbers


# Calculating the sum of part numbers
part_numbers = get_part_numbers()
print("Part numbers:", part_numbers)
print("Sum of part numbers:", sum(part_numbers))

# I had a little help cleaning this one up :)
