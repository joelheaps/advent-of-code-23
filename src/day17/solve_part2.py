from dataclasses import dataclass
import sys
from reader import input_data
from enum import Enum, auto
import heapq


# Constants
MAX_COST: int = sys.maxsize


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

    def __lt__(self, other):
        return False


OPPOSITE_DIRECTIONS: dict = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.NONE: None,
}


@dataclass
class Grid:
    """Represents the grid of blocks."""

    blocks: list[list[int]]

    def exists(self, coords: tuple[int, int]) -> bool:
        """Returns the value of the block at the given coordinates, or None if out of bounds."""
        row, col = coords
        if row < 0 or col < 0:
            return False
        try:
            if self.blocks[row][col]:
                return True
        except IndexError:
            return False
        return False

    def get_value(self, coords: tuple[int, int]) -> int | None:
        """Returns the value of the block at the given coordinates, or None if out of bounds."""
        row, col = coords
        return self.blocks[row][col]

    def get_all_blocks(self) -> list[tuple[int, int]]:
        """Returns coordinates for all blocks in the grid."""
        return [
            (row, col)
            for row in range(len(self.blocks))
            for col in range(len(self.blocks[0]))
        ]

    def get_neighbors(self, coords: tuple[int, int, Direction, int]) -> list[
        tuple[
            tuple[int, int, Direction, int],  # coords, direction, steps
            int,  # weight
        ]
    ]:
        row, col, direction, steps = coords
        neighbors = []

        for delta_row, delta_col, new_direction in [
            (1, 0, Direction.DOWN),
            (-1, 0, Direction.UP),
            (0, 1, Direction.RIGHT),
            (0, -1, Direction.LEFT),
        ]:
            new_row = row + delta_row
            new_col = col + delta_col

            if self.exists((new_row, new_col)):
                if new_direction == direction:
                    new_steps = steps + 1
                else:
                    new_steps = 1

                if new_steps <= 10:
                    if (
                        (new_steps >= 4)
                        or (steps >= 4)
                        or (new_direction == direction)
                        or (direction == Direction.NONE)
                    ):
                        if (
                            not OPPOSITE_DIRECTIONS[direction] == new_direction
                        ):  # Don't reverse
                            neighbors.append(
                                (
                                    (new_row, new_col, new_direction, new_steps),
                                    self.get_value((new_row, new_col)),
                                )
                            )

        return neighbors


def dijkstra(grid: Grid, start: tuple[int, int, Direction, int]):
    # This dictionary will store the shortest path to a node
    path_cost = {}
    path_cost[start] = 0
    predecessors = {}

    # This priority queue will store tuples of (distance, block)
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_block = heapq.heappop(priority_queue)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        if current_distance > path_cost[current_block]:
            continue

        for neighbor, weight in grid.get_neighbors(current_block):
            distance = current_distance + weight

            # Only consider this new path if it's shorter than any path we've
            # already found
            if neighbor not in path_cost:
                path_cost[neighbor] = MAX_COST

            if distance < path_cost[neighbor]:
                path_cost[neighbor] = distance
                predecessors[neighbor] = current_block
                heapq.heappush(priority_queue, (distance, neighbor))

    return predecessors, path_cost


def reconstruct_path(
    previous_blocks: dict[
        tuple[int, int, Direction, int], tuple[int, int, Direction, int]
    ],
    path_cost: dict[tuple[int, int, Direction, int], int],
    start_block: tuple[int, int, Direction, int],
    end_location: tuple[int, int],
) -> list[tuple[int, int, Direction, int]]:
    """Reconstructs the shortest path from start_block to a block at end_location with the lowest path cost."""
    # Find end blocks with the correct location and get the one with the lowest cost
    end_block_candidates = [block for block in path_cost if block[:2] == end_location]
    if not end_block_candidates:
        return []  # No path found

    print(end_block_candidates)
    end_block = min(end_block_candidates, key=lambda b: path_cost[b])
    print(path_cost[end_block])

    path = []
    current_block = end_block
    while current_block != start_block:
        path.append(current_block)
        current_block = previous_blocks.get(current_block, start_block)
    path.append(start_block)
    return path[::-1]


# Visualization
def visualize_path(grid: Grid, path: list[tuple[int, int, Direction, int]]) -> None:
    """Prints the grid with the path marked."""
    path_coords = {(row, col) for row, col, _, _ in path}
    for row in range(len(grid.blocks)):
        for col in range(len(grid.blocks[0])):
            if (row, col) in path_coords:
                print("X", end=" ")
            else:
                print(grid.blocks[row][col], end=" ")
        print()


# Main Function
def main():
    blocks = []
    lines = input_data.splitlines()
    for row in lines:
        row_blocks = []
        for col in row:
            row_blocks.append(int(col))
        blocks.append(row_blocks)

    grid = Grid(blocks)

    start_block = (0, 0, Direction.NONE, 0)

    previous_blocks, path_cost = dijkstra(grid, start_block)
    path = reconstruct_path(
        previous_blocks, path_cost, start_block, (len(lines) - 1, len(lines[0]) - 1)
    )


if __name__ == "__main__":
    main()
