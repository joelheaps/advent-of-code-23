from dataclasses import dataclass, field
from reader import input_data
from enum import Enum, auto
from typing import Self
from copy import deepcopy
from tqdm import tqdm
from pathlib import Path
import csv


@dataclass
class Tile:
    value: str
    energized: bool = False

    def __repr__(self) -> str:
        return self.value


@dataclass
class Grid:
    tiles: list[list[Tile]]

    def get_tile(self, r: int, c: int) -> Tile | None:
        if (r < 0) or (c < 0):
            return None
        try:
            return self.tiles[r][c]
        except IndexError:
            return None

    def energize_tile(self, r: int, c: int) -> None:
        self.tiles[r][c].energized = True

    def display_grid(self) -> None:
        for row in self.tiles:
            for tile in row:
                char = "*" if tile.energized and tile.value == "." else tile.value
                print(char, end=" ")
            print()  # New line after each row

    @property
    def energized_tiles(self) -> list[Tile]:
        tiles = []
        for tile_row in self.tiles:
            tiles += [tile for tile in tile_row if tile.energized]
        return tiles


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Beam:
    r: int = 0
    c: int = -1
    direction: Direction = Direction.RIGHT
    history: set[tuple[int, int, Direction]] = field(default_factory=set)

    def move(self) -> tuple[int, int, Direction]:
        if self.direction == Direction.UP:
            self.r -= 1
        elif self.direction == Direction.DOWN:
            self.r += 1
        elif self.direction == Direction.LEFT:
            self.c -= 1
        elif self.direction == Direction.RIGHT:
            self.c += 1

        return self.r, self.c, self.direction

    def interact_with_tile(self, tile: Tile) -> list[Self] | None:
        if tile.value == "/":
            for pair in [
                {Direction.RIGHT, Direction.UP},
                {Direction.LEFT, Direction.DOWN},
            ]:
                if self.direction in pair:
                    pair.remove(self.direction)
                    self.direction = list(pair)[0]
        elif tile.value == "\\":
            for pair in [
                {Direction.RIGHT, Direction.DOWN},
                {Direction.LEFT, Direction.UP},
            ]:
                if self.direction in pair:
                    pair.remove(self.direction)
                    self.direction = list(pair)[0]
        elif tile.value == "-":
            if self.direction in {Direction.UP, Direction.DOWN}:
                return [
                    Beam(self.r, self.c, Direction.LEFT, self.history),
                    Beam(self.r, self.c, Direction.RIGHT, self.history),
                ]
        elif tile.value == "|":
            if self.direction in {Direction.LEFT, Direction.RIGHT}:
                return [
                    Beam(self.r, self.c, Direction.UP, self.history),
                    Beam(self.r, self.c, Direction.DOWN, self.history),
                ]

    def update(self, grid: Grid) -> tuple[bool, list[Self] | None]:
        new_loc = self.move()

        # Check location history for loops
        if new_loc in self.history:
            return True, None  # Looped (true), no new beams
        else:
            self.history.add(new_loc)

        # Get new tile and interact with it, or exit if none found
        current_tile: Tile | None = grid.get_tile(self.r, self.c)
        if current_tile:
            grid.energize_tile(self.r, self.c)
            interact_result = self.interact_with_tile(current_tile)
        else:
            return True, None  # Exited gird (true), no new beams

        return False, interact_result  # Still in grid, possible new beams


def main():
    tiles = []
    for row in input_data.splitlines():
        tiles.append([Tile(char) for char in row])

    grid = Grid(tiles)

    beams = [Beam()]
    new_beams = []

    while tqdm(beams):
        current_beam = beams.pop(0)
        exited_or_looped = False
        next_beam = False

        while not (exited_or_looped or next_beam):
            exited_or_looped, beam_splits = current_beam.update(grid)
            if beam_splits:
                new_beams.extend(beam_splits)
                next_beam = True

        if new_beams:
            beams.extend(new_beams)
            new_beams = []

    grid.display_grid()
    print(len(grid.energized_tiles))


def get_init_scenarios(grid: Grid):
    init_vals: list[tuple[int, int, Direction]] = []

    for r in range(len(grid.tiles)):
        init_vals.append((r, -1, Direction.RIGHT))
        init_vals.append((r, len(grid.tiles[0]), Direction.LEFT))

    for c in range(len(grid.tiles[0])):
        init_vals.append((-1, c, Direction.DOWN))
        init_vals.append((len(grid.tiles), c, Direction.UP))

    return init_vals


def write_init_to_csv(data, file_name="output.csv"):
    # Determine the size of the table
    max_row = max(data, key=lambda x: x[0])[0] + 1
    max_col = max(data, key=lambda x: x[1])[1] + 1

    # Create the table with placeholders, adding an offset of +1
    table = [[" " for _ in range(max_col + 1)] for _ in range(max_row + 1)]

    # Fill the table with directions, considering the offset
    for y, x, direction in data:
        table[y + 1][x + 1] = direction.name[0]  # Use the first letter of the direction

    # Write to CSV
    with Path(file_name).open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(table)


def main_2():
    tiles = []
    for row in input_data.splitlines():
        tiles.append([Tile(char) for char in row])

    init_grid = Grid(tiles)

    totals = []

    for r, c, direction in tqdm(get_init_scenarios(init_grid)):
        grid = deepcopy(init_grid)

        beams = [Beam(r, c, direction)]

        new_beams = []

        while beams:
            current_beam = beams.pop(0)
            exited_or_looped = False
            next_beam = False

            while not (exited_or_looped or next_beam):
                exited_or_looped, beam_splits = current_beam.update(grid)
                if beam_splits:
                    new_beams.extend(beam_splits)
                    next_beam = True

            if new_beams:
                beams.extend(new_beams)
                new_beams = []

        totals.append(len(grid.energized_tiles))

    print(totals)
    print(max(totals))


if __name__ == "__main__":
    main_2()
