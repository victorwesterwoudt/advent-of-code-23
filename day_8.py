from collections import defaultdict
from enum import Enum
from functools import cached_property, reduce
from math import gcd

from src import Day


class Direction(Enum):
    def __new__(cls, value: str, idx: int):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.idx = idx
        return obj

    L = ("L", 0)
    R = ("R", 1)


class Node:
    def __init__(self, line: str) -> None:
        self._line = line
        source, dest = line.split(" = ")
        self._source = source.strip()
        self._dest = dest[1:-1].split(", ")

    def __repr__(self) -> str:
        return f"{self._source} -> ({self._dest[0]}, {self._dest[1]})"

    def __eq__(self, __value: object) -> bool:
        return self._source == __value

    def __getitem__(self, idx: int) -> str:
        return self._source[idx]

    def move(self, direction: Direction):
        return self._dest[direction.idx]

    @property
    def L(self):
        return self.move(Direction.L)

    @property
    def R(self):
        return self.move(Direction.R)


class Network:
    def __init__(self, nodes: list[Node]) -> None:
        self._nodes = defaultdict(str)
        for node in nodes:
            self._nodes[node._source] = node

    def __getitem__(self, idx: str) -> Node:
        return self._nodes[idx]


class Day8(Day):
    @cached_property
    def instructions(self):
        return [Direction[x] for x in self.raw_data[0]]

    @cached_property
    def network(self):
        return Network(self.nodes)

    @cached_property
    def nodes(self):
        return [Node(x) for x in self.raw_data[2::]]

    def part_1(self):
        node = self.network["AAA"]
        i = 0
        while node != "ZZZ":
            node = self.network[
                node.move(self.instructions[i % len(self.instructions)])
            ]
            i += 1
        return i

    def lcm(self, a, b):
        return a * b // gcd(a, b)

    def part_2(self):
        nodes = list(filter(lambda x: x[-1] == "A", self.nodes))
        loops = []
        for node in nodes:
            i = 0
            while node[-1] != "Z":
                node = self.network[
                    node.move(self.instructions[i % len(self.instructions)])
                ]
                i += 1
            loops.append(i)

        return reduce(self.lcm, loops)


if __name__ == "__main__":
    d = Day8("./input/day_8.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
