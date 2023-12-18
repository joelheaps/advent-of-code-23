from dataclasses import dataclass, field
from reader import input_data
from enum import Enum, auto
from typing import Self
from copy import deepcopy
from tqdm import tqdm
from pathlib import Path
import csv


@dataclass
class Block:
    value: str
    visited: bool = False

    def __repr__(self) -> str:
        return self.value


@dataclass
class Grid:
    blocks: list[list[Block]]

    def get_block(self, r: int, c: int) -> Block | None:
        if (r < 0) or (c < 0):
            return None
        try:
            return self.blocks[r][c]
        except IndexError:
            return None

    def visit_block(self, r: int, c: int) -> None:
        self.blocks[r][c].visited = True

    def visited_blocks(self) -> None:
        for row in self.blocks:
            for block in row:
                char = "*" if block.visited and block.value == "." else block.value
                print(char, end=" ")
            print()  # New line after each row

    @property
    def visited_blocks(self) -> list[Block]:
        blocks = []
        for block_row in self.blocks:
            blocks += [block for block in block_row if block.visited]
        return blocks


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class DrivingPath:
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

    def get_options(self, block: Block) -> list[Self] | None: ...

    def update(self, grid: Grid) -> tuple[bool, list[Self] | None]:
        new_loc = self.move()

        # Check location history for loops
        if new_loc in self.history:
            return True, None  # Looped (true), no new paths
        else:
            self.history.add(new_loc)

        # Get new block and interact with it, or exit if none found
        current_block: Block | None = grid.get_block(self.r, self.c)
        if current_block:
            grid.energize_block(self.r, self.c)
            interact_result = self.interact_with_block(current_block)
        else:
            return True, None  # Exited gird (true), no new paths

        return False, interact_result  # Still in grid, possible new paths


def main():
    blocks = []
    for row in input_data.splitlines():
        blocks.append([Block(char) for char in row])

    grid = Grid(blocks)

    paths = [DrivingPath()]
    new_paths = []

    while tqdm(paths):
        current_path = paths.pop(0)
        exited_or_looped = False
        next_path = False

        while not (exited_or_looped or next_path):
            exited_or_looped, path_splits = current_path.update(grid)
            if path_splits:
                new_paths.extend(path_splits)
                next_path = True

        if new_paths:
            paths.extend(new_paths)
            new_paths = []

    grid.display_grid()
    print(len(grid.visited_blocks))


def get_init_scenarios(grid: Grid):
    init_vals: list[tuple[int, int, Direction]] = []

    for r in range(len(grid.blocks)):
        init_vals.append((r, -1, Direction.RIGHT))
        init_vals.append((r, len(grid.blocks[0]), Direction.LEFT))

    for c in range(len(grid.blocks[0])):
        init_vals.append((-1, c, Direction.DOWN))
        init_vals.append((len(grid.blocks), c, Direction.UP))

    return init_vals


def main_2():
    blocks = []
    for row in input_data.splitlines():
        blocks.append([Block(char) for char in row])

    init_grid = Grid(blocks)

    totals = []

    for r, c, direction in tqdm(get_init_scenarios(init_grid)):
        grid = deepcopy(init_grid)

        paths = [DrivingPath(r, c, direction)]

        new_paths = []

        while paths:
            current_path = paths.pop(0)
            exited_or_looped = False
            next_path = False

            while not (exited_or_looped or next_path):
                exited_or_looped, path_splits = current_path.update(grid)
                if path_splits:
                    new_paths.extend(path_splits)
                    next_path = True

            if new_paths:
                paths.extend(new_paths)
                new_paths = []

        totals.append(len(grid.visited_blocks))

    print(totals)
    print(max(totals))


if __name__ == "__main__":
    main_2()
