from reader import input_data
from dataclasses import dataclass


def holiday_hash(s: str) -> int:
    """
    Start with current value of 0.
    Then for each char:
        Determine the ASCII code for the current character of the string.
        Increase the current value by the ASCII code you just determined.
        Set the current value to itself multiplied by 17.
        Set the current value to the remainder of dividing itself by 256.
    """
    current_value: int = 0
    for char in s:
        current_value = current_value + ord(char)
        current_value = current_value * 17
        current_value = current_value % 256
    return current_value


@dataclass
class Lens:
    label: str
    focal_length: int

    @property
    def loc(self) -> int:
        return holiday_hash(self.label)


def replace_lens(box: list[int], lens: Lens, pop: bool = False) -> list[int]:
    for i in range(len(box)):
        if box[i].label == lens.label:
            if pop:
                box.pop(i)
                return box

            box[i] = lens
    return box


def main_1():
    hashes: list[int] = [holiday_hash(s) for s in input_data.split(",")]
    print("sum:", sum(hashes))


def main_2():
    boxes: dict[int, list[int]] = {}  # 256 boxes

    for instruction in input_data.split(","):
        if "=" in instruction:
            split = instruction.split("=")
            lens = Lens(label=split[0], focal_length=int(split[1]))

            if lens.loc in boxes:
                if lens.label in [lens.label for lens in boxes[lens.loc]]:
                    # Swap lens if label exists already
                    boxes[lens.loc] = replace_lens(boxes[lens.loc], lens)
                else:
                    # Add to end if box exists but label doesn't yet
                    boxes[lens.loc].append(lens)
            else:
                # Initialize box
                boxes[lens.loc] = [lens]
        elif "-" in instruction:
            # Remove lens
            instruction = instruction.replace("-", "")
            lens = Lens(label=instruction, focal_length=0)
            if lens.loc in boxes:
                boxes[lens.loc] = replace_lens(boxes[lens.loc], lens, pop=True)

    for key, value in dict(sorted(boxes.items())).items():
        print(f"box {key}: {[f'{lens.label}:{lens.focal_length}' for lens in value]}")

    # get power
    lens_powers: list[int] = []
    for box_n, lenses in boxes.items():
        for i in range(len(lenses)):
            power = box_n + 1
            power = power * (i + 1)
            power = power * lenses[i].focal_length
            lens_powers.append(power)

    print("total power:", sum(lens_powers))


if __name__ == "__main__":
    main_2()
