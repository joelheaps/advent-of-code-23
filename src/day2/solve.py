from dataclasses import dataclass
from pathlib import Path

INPUT: Path = Path("input.txt")


@dataclass
class CubeSet:
    red_cubes: int = 0
    green_cubes: int = 0
    blue_cubes: int = 0

    def check_if_possible(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return (
            self.red_cubes <= max_red
            and self.green_cubes <= max_green
            and self.blue_cubes <= max_blue
        )


@dataclass
class Game:
    game_id: int
    sets: list[CubeSet]
    max_red_cubes: int = 12
    max_green_cubes: int = 13
    max_blue_cubes: int = 14

    @property
    def possible(self) -> bool:
        sets_possible: list[bool] = []
        for cube_set in self.sets:
            sets_possible.append(
                cube_set.check_if_possible(
                    self.max_red_cubes, self.max_green_cubes, self.max_blue_cubes
                )
            )

        return all(sets_possible)

    @property
    def min_red(self) -> int:
        return max([_set.red_cubes for _set in self.sets])

    @property
    def min_green(self) -> int:
        return max([_set.green_cubes for _set in self.sets])

    @property
    def min_blue(self) -> int:
        return max([_set.blue_cubes for _set in self.sets])

    @property
    def power_of_mins(self) -> int:
        return self.min_red * self.min_green * self.min_blue


def parse_raw_set(substring: str) -> CubeSet:
    substring = substring.replace(" ", "")
    cube_groups = substring.split(",")
    cubeset = CubeSet()

    for group in cube_groups:
        if "red" in group:
            group = group.replace("red", "")
            cubeset.red_cubes = int(group)
        elif "blue" in group:
            group = group.replace("blue", "")
            cubeset.blue_cubes = int(group)
        elif "green" in group:
            group = group.replace("green", "")
            cubeset.green_cubes = int(group)

    return cubeset


def parse_game_line(line: str) -> Game:
    # Get game ID
    line = line.replace("Game ", "")
    split_line: list[str] = line.split(":")
    game_id = int(split_line[0])

    # Get sets
    sets_raw: list[str] = split_line[1].split(";")
    cubesets: list[CubeSet] = []
    for _set in sets_raw:
        cubesets.append(parse_raw_set(_set))

    return Game(game_id=game_id, sets=cubesets)


def main() -> None:
    games: list[Game] = []
    with INPUT.open("r") as file:
        for line in file.readlines():
            games.append(parse_game_line(line))

    possible_game_ids: list[int] = [game.game_id for game in games if game.possible]
    minimum_cube_powers: list[int] = [game.power_of_mins for game in games]

    print(f"Sum of possible games: {sum(possible_game_ids)}")
    print(f"Sum of powers of minimum cube counts: {sum(minimum_cube_powers)}")


if __name__ == "__main__":
    main()
