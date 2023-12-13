from dataclasses import dataclass

NUMBERS: str = "1234567890"
NOT_SYMBOLS: str = NUMBERS + "."


def symbol_adjacent(line: str, first: int, last: int) -> bool:
    """Checks whether a symbol is directly touching the specified range in the current line."""
    return (line[first - 1] not in NOT_SYMBOLS) or (line[last + 1] not in NOT_SYMBOLS)


def is_valid_part_loc(string: str, line_n: int, first: int, last: int) -> bool:
    lines = string.splitlines()
    test_cases: list[bool] = []

    # check previous line
    prev_line_n: int = line_n - 1
    if prev_line_n >= 0:
        test_cases.append(symbol_adjacent(lines[prev_line_n], first, last))

    # check current line
    test_cases.append(symbol_adjacent(lines[line_n], first, last))

    # check next line:
    next_line_n = line_n + 1
    if next_line_n <= len(lines):
        test_cases.append(symbol_adjacent(lines[next_line_n], first, last))

    return any(test_cases)
