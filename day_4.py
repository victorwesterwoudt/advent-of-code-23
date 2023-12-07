from collections import defaultdict
from functools import cached_property

from src import Day


class Day4(Day):
    @cached_property
    def data(self):
        data = defaultdict()

        for line in self.raw_data:
            c, line = line.split(":")
            card = int(c.split()[-1])
            nums, wins = line.split("|")
            nums = [int(n.strip()) for n in nums.split()]
            wins = [int(w.strip()) for w in wins.split()]

            data[card] = list(set(nums) & set(wins))

        return data

    def part_1(self):
        return sum(
            [
                2 ** (len(card) - 1)
                for _, card in self.data.items()
                if len(card) > 0
            ]
        )

    def part_2(self):
        copies = defaultdict(int)
        for card, wins in self.data.items():
            copies[card] += 1
            for j in range(len(wins)):
                if card + j + 1 in self.data:
                    copies[card + j + 1] += copies[card]

        return sum(copies.values())


if __name__ == "__main__":
    d = Day4("./input/day_4.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 1: {d.part_2()}")
