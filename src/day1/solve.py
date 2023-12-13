from pathlib import Path


INPUT: Path = Path("puzzle_input.txt")
DIGITS: str = "1234567890"
WORD_DIGITS: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_first_letter_list(word_list: list[str]) -> list[str]:
    letters: list[str] = []
    for word in word_list:
        letters.append(word[0])

    return letters


STARTING_LETTERS: list[str] = get_first_letter_list(WORD_DIGITS.keys())


def check_if_next_word_is_number(substring: str) -> int | None:
    for word, value in WORD_DIGITS.items():
        if word[0] == substring[0] and len(substring) >= 3:
            check_length: int = len(word)
            print(
                f"Checking substring {substring[:check_length]} in string"
                f" {substring} for {word}"
            )
            if substring[:check_length] == word:
                print("Found")
                return value


def get_digits(line: str) -> str:
    line_digits = []

    for i in range(len(line)):
        if line[i] in DIGITS:
            line_digits.append(line[i])
        elif line[i] in STARTING_LETTERS:
            print(f"Found interesting char {line[i]} in line")
            possible_num: int | None = check_if_next_word_is_number(line[i:])
            if possible_num:
                line_digits.append(possible_num)

    if not line_digits:
        return ""

    return f"{line_digits[0]}{line_digits[-1]}"


def sum_all(line_digits: list[str]) -> int:
    sum: int = 0

    for line in line_digits:
        if line:
            sum += int(line)

    return sum


def main() -> None:
    all_line_digits = []

    with INPUT.open() as file:
        for line in file.readlines():
            all_line_digits.append(get_digits(line))

    sum: int = sum_all(all_line_digits)

    print(f"Sum of all lines: {sum}")


if __name__ == "__main__":
    main()
