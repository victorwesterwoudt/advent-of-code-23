import math

from src import Day


class Day6(Day):
    @property
    def data1(self):
        times = [int(x) for x in self.raw_data[0].split(":")[1].split()]
        distances = [int(x) for x in self.raw_data[1].split(":")[1].split()]

        return times, distances

    @property
    def data2(self):
        return [int("".join(map(str, x))) for x in self.data1]

    @staticmethod
    def solve(t, d):
        sols = sorted(
            [
                (-t + (t**2 - 4 * d) ** 0.5) / 2,
                (-t - (t**2 - 4 * d) ** 0.5) / 2,
            ]
        )

        sols = math.ceil(sols[0]), math.floor(sols[1])

        return sols[1] - sols[0] + 1

    def part_1(self):
        opts = 1
        for t, d in zip(*self.data1):
            opts *= self.solve(t, d)
        return opts

    def part_2(self):
        return self.solve(*self.data2)


if __name__ == "__main__":
    d = Day6("./input/day_6.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
