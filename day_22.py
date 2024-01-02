from src import Day
from functools import cached_property
from collections import deque


class Brick(object):
    def __init__(self, definition: str) -> None:
        self._definition = definition
        s, e = [
            tuple([int(x) for x in y.split(",")])
            for y in definition.split("~")
        ]
        self.x = range(s[0], e[0] + 1)
        self.y = range(s[1], e[1] + 1)
        self.z = range(s[2], e[2] + 1)

    def __repr__(self) -> str:
        return (
            f"Brick({self.x.start},{self.y.start},"
            f"{self.z.start}~{self.x.stop-1},"
            f"{self.y.stop-1},{self.z.stop-1})"
        )

    def __hash__(self) -> int:
        return hash(self._definition)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Brick):
            return False
        return self._definition == __value._definition

    @cached_property
    def footprint(self):
        return {(x, y) for x in self.x for y in self.y}

    def lower(self, n: int = 1) -> "Brick":
        self.z = range(self.z.start - n, self.z.stop - n)
        return self

    def overlap(self, bricks: list["Brick"], reverse=False, below=True):
        if below:
            bricks = [b for b in bricks if b.z.stop <= self.z.start]

        overlap = [
            b for b in bricks if b.footprint & self.footprint and b != self
        ]
        return sorted(overlap, key=lambda b: b.z.stop, reverse=reverse)


class Day22(Day):
    def __init__(self, input_file: str) -> None:
        super().__init__(input_file)
        bricks = [Brick(line) for line in self.raw_data]
        self.bricks = sorted(bricks, key=lambda b: b.z.stop)

    @cached_property
    def supported_by(self) -> dict["Brick", list["Brick"]]:
        supported_by = {}

        for brick in self.bricks:
            below = brick.overlap(self.bricks, below=True)

            if not below and brick.z.start > 1:
                brick.lower(brick.z.start - 1)
            elif below and (n := brick.z.start - below[-1].z.stop) > 0:
                brick.lower(n)

            supported_by[brick] = [
                b for b in below if b.z.stop == brick.z.start
            ]

        return supported_by

    def part_1(self):
        criticalsupports = set()
        for v in self.supported_by.values():
            if len(v) == 1:
                criticalsupports.add(v[0])

        return len(set(d.bricks) - criticalsupports)

    def part_2(self):
        score = {}
        for brick in self.bricks:
            queue = deque([brick])
            destroyed = set()
            while queue:
                br = queue.pop()
                destroyed.add(br)
                dependents = [
                    b for b, s in self.supported_by.items() if br in s
                ]
                for d in dependents:
                    if not set(self.supported_by[d]) - destroyed:
                        queue.append(d)

            score[brick] = len(destroyed) - 1
        return sum(score.values())


if __name__ == "__main__":
    d = Day22("./input/day_22.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
