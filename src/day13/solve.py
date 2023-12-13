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


def check_all_rows_for_symmetry_at_column(pattern: str, column_n: int) -> bool:
    rows: list[str] = pattern.splitlines()
    test_cases: list[bool] = []

    for row in rows:
        result: bool = check_row_symmetry_at_column(row, column_n)
        test_cases.append(result)

    return all(test_cases)


def find_symmetry_column(pattern: str) -> int | None:
    """Returns column number whose left edge is the line of symmetry (if any)."""
    width: int = len(pattern.splitlines()[0])

    for column_n in range(width):
        if check_all_rows_for_symmetry_at_column(pattern, column_n):
            return column_n
