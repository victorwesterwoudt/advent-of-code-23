from src import Day
from functools import cached_property
from enum import Enum


class Direction(Enum):
    idx: int
    delta: tuple[int, int]

    def __new__(cls, value, idx, delta):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.idx = idx
        obj.delta = delta
        return obj

    def __repr__(self) -> str:
        return f"{self.value}"

    UP = ("U", 3, (-1, 0))
    RIGHT = ("R", 0, (0, 1))
    LEFT = ("L", 2, (0, -1))
    DOWN = ("D", 1, (1, 0))

    @classmethod
    def from_index(cls, index):
        for direction in cls:
            if direction.idx == index:
                return direction
        raise ValueError("Invalid index")


class Day18(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            d, s, c = line.split()
            s = int(s)
            temp = c.strip("()").strip("#")
            c = (Direction.from_index(int(temp[5:], 16)), int(temp[0:5], 16))
            d = Direction(d)
            output.append((d, s, c))
        return output

    @staticmethod
    def next(start: tuple[int, int], direction: Direction, n: int, *args):
        return tuple([x + n * y for x, y in zip(start, direction.delta)])

    @staticmethod
    def area(loop):
        return int(
            0.5
            * abs(
                sum(
                    x0 * y1 - x1 * y0
                    for (x0, y0), (x1, y1) in zip(loop, loop[1:] + loop[:1])
                )
            )
        )

    def polygon(self, part_2=False):
        vertices = [(0, 0)]
        for move in self.data:
            vertices.append(
                self.next(vertices[-1], *move)
                if not part_2
                else self.next(vertices[-1], *move[2])
            )

        return vertices

    def part_1(self):
        return (
            self.area(self.polygon())
            + int(sum([x[1] for x in self.data]) / 2)
            + 1
        )

    def part_2(self):
        return (
            self.area(self.polygon(part_2=True))
            + int(sum([x[2][1] for x in d.data]) / 2)
            + 1
        )


if __name__ == "__main__":
    d = Day18("./input/day_18.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
