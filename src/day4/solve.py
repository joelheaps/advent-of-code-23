from reader import input_data

INPUT_LINES = input_data.splitlines()


def parse_card(line: str) -> tuple[list[int], list[int]]:
    n = line.split(":")[1].strip()
    split_n = n.split("|")
    win_n = split_n[0].strip().split(" ")
    my_n = split_n[1].strip().split(" ")

    return [int(n) for n in win_n if n], [int(n) for n in my_n if n]


def get_value(win_n: list[int], my_n: list[int]) -> int:
    my_winning_numbers = [n for n in my_n if n in win_n]
    if my_winning_numbers:
        return 2 ** (len(my_winning_numbers) - 1)

    return 0


def main():
    card_values: list[int] = []
    for line in INPUT_LINES:
        win_n, my_n = parse_card(line)
        card_values.append(get_value(win_n, my_n))

    print(sum(card_values))


if __name__ == "__main__":
    main()
