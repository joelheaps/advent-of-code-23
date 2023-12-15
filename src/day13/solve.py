import numpy as np
from pathlib import Path


INPUT: Path = Path("input.txt")
PART: int = 1


def mirror_left_side(row: str, column_n: int) -> str:
    """Mirrors everything left of the specified column."""
    substring = row[:column_n]
    return substring[::-1]


def check_row_symmetry_at_column(row: str, column_n: int) -> bool:
    """Checks whether columns left of row, when mirrored, equal columns right of row
    (inclusive)."""
    left_mirror: str = mirror_left_side(row, column_n)
    right_remaining: str = row[column_n:]
    min_length: int = min([len(left_mirror), len(right_remaining)])
    if min_length == 0:
        return False

    # Trim to min length
    left_trimmed = left_mirror[:min_length]  # already flipped, treat as right string
    right_trimmed = right_remaining[:min_length]

    return left_trimmed == right_trimmed


def check_all_rows_for_symmetry_at_column(
    pattern: str, column_n: int, one_off: bool = False
) -> bool:
    rows: list[str] = pattern.splitlines()
    test_cases: list[bool] = []

    for row in rows:
        result: bool = check_row_symmetry_at_column(row, column_n)
        test_cases.append(result)

    if one_off:
        return True if test_cases.count(False) == 1 else False

    return all(test_cases)


def find_symmetry_column(pattern: str, one_off: bool = False) -> int | None:
    """Returns column number whose left edge is the line of symmetry (if any)."""
    width: int = len(pattern.splitlines()[0])

    for column_n in range(width):
        if check_all_rows_for_symmetry_at_column(pattern, column_n, one_off):
            return column_n


def rotate_str(string: str, reverse: bool = False) -> list[list]:
    n_times: int = 3 if reverse else 1
    rows: list[list[str]] = [
        list(row) for row in string.splitlines()
    ]  # Split strings into lists
    rotated_rows: list[list[str]] = np.rot90(rows, n_times)
    return "\n".join(["".join(row) for row in rotated_rows])


def find_symmetry_row(pattern: str, one_off: bool = False) -> int | None:
    pattern = rotate_str(pattern)
    return find_symmetry_column(pattern, one_off)


def parse_patterns(file: Path) -> list[str]:
    with file.open("r") as f:
        contents: str = f.read()
        return contents.split("\n\n")


def main_2():
    patterns: list[str] = parse_patterns(INPUT)

    columns_left: list[int] = []
    rows_above: list[int] = []

    for pattern in patterns:
        # Find new lines of symmetry (with smudges) in patterns that never matched
        if find_symmetry_row(pattern, one_off=True):
            row_n = find_symmetry_row(pattern, one_off=True)
            if row_n:
                print(f"Found new symmetry row {row_n} in pattern \n{pattern}")
                rows_above.append(row_n)

        else:
            column_n = find_symmetry_column(pattern, one_off=True)
            if column_n:
                print(f"Found new symmetry row {column_n} in pattern \n{pattern}")
                columns_left.append(column_n)

    print(f"Sum of columns left of symmetry lines: {sum(columns_left)}")
    print(
        f"Sum of rows above symmetry lines: {sum(rows_above)}, * 100 = {sum(rows_above) * 100}"
    )
    print(f"Sum of both: {sum(columns_left) + (100 * sum(rows_above))}")


def main_1():
    patterns: list[str] = parse_patterns(INPUT)

    columns_left: list[int] = []
    rows_above: list[int] = []

    for pattern in patterns:
        column_n = find_symmetry_column(pattern)

        if column_n:
            columns_left.append(column_n)
        else:
            row_n = find_symmetry_row(pattern)

            if row_n:
                rows_above.append(row_n)

    print(f"Sum of columns left of symmetry lines: {sum(columns_left)}")
    print(
        f"Sum of rows above symmetry lines: {sum(rows_above)}, * 100 = {sum(rows_above) * 100}"
    )
    print(f"Sum of both: {sum(columns_left) + (100 * sum(rows_above))}")


if __name__ == "__main__":
    if PART == 1:
        main_1()
    else:
        main_2()
