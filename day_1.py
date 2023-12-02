import re
from enum import Enum

from src import Day


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


class Day1(Day):
    """
    Class representing the solution for Day 1 of the Advent of Code challenge.
    """

    @property
    def data(self) -> list:
        """
        Get the raw data for the challenge.

        Returns:
            list: The raw data.
        """
        return self.raw_data

    @staticmethod
    def _filter_data(data: list) -> list:
        """
        Filter the data by removing non-digit characters.

        Args:
            data (list): The data to filter.

        Returns:
            list: The filtered data.
        """
        return [re.sub(r"\D", "", line) for line in data]

    @classmethod
    def _numerize(cls, data: list) -> list:
        """
        Convert the filtered data into a list of numbers.

        Args:
            data (list): The filtered data.

        Returns:
            list: The numerized data.
        """
        return [int(x[0]) * 10 + int(x[-1]) for x in cls._filter_data(data)]

    def part_1(self) -> int:
        """
        Solve part 1 of the challenge.

        Returns:
            int: The solution for part 1.
        """
        return sum(self._numerize(self.data))

    def part_2(self) -> int:
        """
        Solve part 2 of the challenge.

        The trick here is that the strings of digits that are being replaced by numbers
        can have their characters overlap with the string of another digit. For example,
        "eightwo" should be replaced with "82". This is why replacing the whole world 
        with a number doesn't work. Instead, we need to replace the middle characters of the 
        number and leave the first and last characters intact.

        Returns:
            int: The solution for part 2.
        """
        temp = self.data
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
    d1 = Day1("./input/day_1.txt")
    print(f"Part 1: {d1.part_1()}")
    print(f"Part 2: {d1.part_2()}")
