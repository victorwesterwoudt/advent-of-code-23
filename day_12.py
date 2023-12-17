from src import Day
from functools import cached_property


class Day12(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            r, g = line.split()
            g = tuple([int(x) for x in g.split(",")])
            output.append((r, g))

        return output

    def solve(self, row: str, groups: tuple, prev_sol={}):
        if (row, groups) in prev_sol:
            return prev_sol[(row, groups)]

        solutions = 0
        if not groups:
            if "#" not in row:
                return 1
            else:
                return 0

        elif "." not in row and len(groups) == 1 and len(row) == groups[0]:
            return 1

        n = groups[0]

        if len(row.replace(".", "")) < sum(groups):
            # dead end
            return 0

        if ("." not in row[:n]) and (row[n] != "#"):
            solutions += self.solve(row[n + 1 :], groups[1:], prev_sol)

        if row[0] != "#":
            solutions += self.solve(row[1:], groups, prev_sol)

        prev_sol[(row, groups)] = solutions

        return solutions

    def part_1(self):
        output = 0
        for row, groups in self.data:
            output += self.solve(row, groups)
        return output

    def part_2(self):
        output = 0
        for row, groups in self.data:
            row = "?".join([row] * 5)
            groups = groups * 5
            output += self.solve(row, groups)
        return output


if __name__ == "__main__":
    d = Day12("./input/day_12.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
