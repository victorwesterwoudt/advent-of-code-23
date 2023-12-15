from src import Day
from functools import cached_property
from collections import deque
from enum import Enum


class Pipe(Enum):
    directions: tuple[tuple[int, int], tuple[int, int]]

    def __new__(cls, value: str, directions: tuple[tuple[int, int], ...]):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.directions = directions
        return obj

    def __repr__(self) -> str:
        return f"{self._value_}"

    VERTICAL = ("|", ((1, 0), (-1, 0)))
    HORIZONTAL = ("-", ((0, 1), (0, -1)))
    NORTH_EAST = ("L", ((0, 1), (-1, 0)))
    NORTH_WEST = ("J", ((0, -1), (-1, 0)))
    SOUTH_WEST = ("7", ((0, -1), (1, 0)))
    SOUTH_EAST = ("F", ((0, 1), (1, 0)))
    GROUND = (".", ())
    START = ("S", ((1, 0), (-1, 0), (0, -1), (0, 1)))


class Day10(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            output.append([Pipe(x) for x in line])

        return output

    @property
    def start(self):
        for idx, line in enumerate(self.data):
            for jdx, pipe in enumerate(line):
                if pipe == Pipe.START:
                    return pipe, (idx, jdx)

    def __getitem__(self, idx: tuple[int, int]):
        return self.data[idx[0]][idx[1]], idx

    def _neighbours(self, node: tuple[Pipe, tuple[int, int]]):
        pipe, loc = node
        neighbours = []

        for direction in pipe.directions:
            ln = (loc[0] + direction[0], loc[1] + direction[1])
            if (ln[0] < 0 or ln[1] < 0) or (
                ln[0] >= len(self.data) or ln[1] >= len(self.data[ln[0]])
            ):
                continue

            neighbours.append(self[ln])

        return neighbours

    def _next(self, node: tuple[Pipe, tuple[int, int]]):
        neighbours = self._neighbours(node)

        for i, n in enumerate(neighbours):
            rns = self._neighbours(n)
            if node not in rns:
                neighbours.pop(i)

        return neighbours

    def plot(self):
        plt = []
        for line in self.data:
            plt.append(["." for x in line])

        for node in self.loop:
            plt[node[1][0]][node[1][1]] = "#"

        return plt

    @cached_property
    def loop(self):
        loop = deque([self.start, self._next(self.start)[0]])
        while True:
            next = list(filter(lambda x: x not in loop, self._next(loop[-1])))
            if len(next) != 0:
                loop.extend(next)
            else:
                break
        return loop

    @property
    def area(self):
        loop = [x[1] for x in self.loop]
        return int(
            0.5
            * abs(
                sum(
                    x0 * y1 - x1 * y0
                    for (x0, y0), (x1, y1) in zip(loop, loop[1:] + loop[:1])
                )
            )
        )

    def part_1(self):
        return len(self.loop) // 2

    def part_2(self):
        return self.area - len(self.loop) // 2 + 1
        pass


if __name__ == "__main__":
    d = Day10("./input/day_10.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
