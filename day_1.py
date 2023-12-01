import re
from enum import Enum

from src import Input, Day


class Digits(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


class Day_1(Day):

    @staticmethod
    def _filter_data(data: list) -> list:
        return [re.sub(r"\D", "", line) for line in data]

    @classmethod
    def _numerize(cls, data: list) -> list:
        return [int(x[0]) * 10 + int(x[-1]) for x in cls._filter_data(data)]

    def part_1(self) -> int:
        return sum(self._numerize(self.raw_data))

    def part_2(self) -> int:
        temp = self.raw_data
        for digit in Digits:
            temp = [
                re.sub(
                    digit.name.lower(),
                    f"{digit.name[0]}{str(digit.value)}{digit.name[-1]}".lower(),
                    line,
                )
                for line in temp
            ]

        return sum(self._numerize(temp))


if __name__ == "__main__":
    d1 = Day_1('./input/day_1.txt')
    print(f"Part 1: {d1.part_1()}")
    print(f"Part 2: {d1.part_2()}")
