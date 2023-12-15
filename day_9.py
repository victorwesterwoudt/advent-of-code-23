from src import Day
from functools import cached_property


class Day9(Day):
    @cached_property
    def data(self):
        lists = []
        for line in self.raw_data:
            lists.append(tuple(map(int, line.split())))
        return lists

    def part_1(self):
        output = 0
        for line in self.data:
            output += self.solve(line)
        return output

    def part_2(self):
        output = 0
        for line in self.data:
            output += self.solve(line, backwards=True)
        return output

    @classmethod
    def solve(cls, lst, backwards=False):
        if all([x == 0 for x in lst]):
            if backwards:
                return lst[0]
            else:
                return lst[-1]
        else:
            delta = [j - i for i, j in zip(lst[:-1], lst[1:])]
            if backwards:
                return lst[0] - cls.solve(delta, backwards)
            else:
                return cls.solve(delta) + lst[-1]


if __name__ == "__main__":
    d = Day9("./input/day_9.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
