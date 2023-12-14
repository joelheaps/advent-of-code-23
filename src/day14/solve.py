import numpy as np
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

INPUT: Path = Path("input.txt")
CYCLES: int = 1000000000


def rotate_str(string: str, clockwise: bool = False) -> list[list]:
    n_times: int = 3 if clockwise else 1
    rows: list[list[str]] = [
        list(row) for row in string.splitlines()
    ]  # Split strings into lists
    rotated_rows: list[list[str]] = np.rot90(rows, n_times)
    return "\n".join(["".join(row) for row in rotated_rows])


def shift_rocks_in_line(line: str) -> str:
    length: int = len(line)
    line: list = list(line)

    left_bound = 0  # Left edge of pattern or square rock (inclusive)
    for i in range(length):
        if line[i] == "#":
            left_bound = i + 1
        if line[i] == "O":
            char = line.pop(i)
            line.insert(left_bound, char)
            left_bound += 1

    return "".join(line)


def slide_rocks_north(pattern: str) -> str:
    """Moves all round rocks as far "up" as they can move, until either a square
    rock or edge is encountered."""

    # rotate string left so rocks can be moved in same line.
    pattern = rotate_str(pattern)

    pattern_lines = pattern.splitlines()

    results = []
    for line in pattern_lines:
        results.append(shift_rocks_in_line(line))

    pattern = "\n".join(results)
    return rotate_str(pattern, clockwise=True)


def slide_rocks_west(pattern: str) -> str:
    """Moves all round rocks as far "up" as they can move, until either a square
    rock or edge is encountered."""
    pattern_lines = pattern.splitlines()

    results = []
    for line in pattern_lines:
        results.append(shift_rocks_in_line(line))

    return "\n".join(results)


def slide_rocks_south(pattern: str) -> str:
    """Moves all round rocks as far "up" as they can move, until either a square
    rock or edge is encountered."""

    # rotate string left so rocks can be moved in same line.
    pattern = rotate_str(pattern, clockwise=True)

    pattern_lines = pattern.splitlines()

    results = []
    for line in pattern_lines:
        results.append(shift_rocks_in_line(line))

    pattern = "\n".join(results)
    return rotate_str(pattern)


def slide_rocks_east(pattern: str) -> str:
    """Moves all round rocks as far "up" as they can move, until either a square
    rock or edge is encountered."""

    # rotate string left so rocks can be moved in same line.
    pattern = rotate_str(rotate_str(pattern))

    pattern_lines = pattern.splitlines()

    results = []
    for line in pattern_lines:
        results.append(shift_rocks_in_line(line))

    pattern = "\n".join(results)
    return rotate_str(rotate_str(pattern))


def get_load(pattern: str) -> int:
    pattern_lines = pattern.splitlines()
    pattern_lines.reverse()

    line_count = len(pattern_lines)

    line_loads = []  # Sum of load for each line

    for i in range(line_count):
        line_load = pattern_lines[i].count("O") * (i + 1)
        line_loads.append(line_load)

    return sum(line_loads)


def main():
    with INPUT.open("r") as f:
        pattern: str = f.read()

    slid_pattern = slide_rocks_north(pattern)
    print(f"{slid_pattern}")

    old_load = get_load(pattern)
    load = get_load(slid_pattern)

    print(f"Old load: {old_load}\nNew load: {load}")


def main_2():
    with INPUT.open("r") as f:
        pattern: str = f.read()

    patterns = {}
    i = 1
    while True:
        pattern = slide_rocks_north(pattern)
        pattern = slide_rocks_west(pattern)
        pattern = slide_rocks_south(pattern)
        pattern = slide_rocks_east(pattern)

        print(f"Adding pattern {i}")
        if pattern in patterns:
            break
        patterns[pattern] = None

        i += 1

    all_possible_patterns_ordered: list[str] = list(patterns.keys())

    remainder = CYCLES % len(all_possible_patterns_ordered)

    pattern = all_possible_patterns_ordered[remainder]

    load = get_load(pattern)

    print(f"{pattern}\n\nRemainder: {remainder}\nLoad: {load}")


if __name__ == "__main__":
    main_2()
