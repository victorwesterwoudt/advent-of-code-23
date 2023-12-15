from src import Day
from collections import defaultdict


class Day11(Day):
    def galaxies(self, expand=1):
        galaxies = []
        ecols = defaultdict(bool)
        i = 0
        for row in self.raw_data:
            j = 0
            if all([x == "." for x in row]):
                i += expand
            else:
                for c, v in enumerate(row):
                    if c not in ecols:
                        col = [x[c] for x in self.raw_data]
                        if all([x == "." for x in col]):
                            ecols[c] = True

                    j += ecols[c] * expand

                    if v == "#":
                        galaxies.append((i, j))

                    j += 1
            i += 1

        return galaxies

    def solve(self, expand=1):
        distances = []
        gs = self.galaxies(expand)
        while len(gs) > 0:
            g = gs.pop()
            for g2 in gs:
                distances.append(abs(g[0] - g2[0]) + abs(g[1] - g2[1]))

        return sum(distances)

    def part_1(self):
        return self.solve()

    def part_2(self):
        return self.solve(1000000 - 1)


if __name__ == "__main__":
    d = Day11("./input/day_11.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
