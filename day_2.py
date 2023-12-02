from src import Day
from functools import reduce
from enum import Enum


class RGB(Enum):
    RED = (0, "red")
    GREEN = (1, "green")
    BLUE = (2, "blue")

    @property
    def color(self) -> str:
        """Get the color string."""
        return self.value[1]

    @property
    def index(self) -> int:
        """Get the index."""
        return str(self.value[0])


class Day2(Day):
    """Class representing Day 2 of the Advent of Code challenge."""

    @property
    def data(self) -> dict:
        """Process the raw data and return a dictionary of game data.

        Returns:
            dict: A dictionary containing game data.
                  The keys are game numbers and the values are 3D
                  lists representing the moves made in each game.
        """
        games = {}
        for line in self.raw_data:
            line = (
                line.replace(RGB.RED.color, RGB.RED.index)
                .replace(RGB.GREEN.color, RGB.GREEN.index)
                .replace(RGB.BLUE.color, RGB.BLUE.index)
            )
            game, sets = line.split(":")
            game = int(game.strip().replace("Game ", ""))
            sets = sets.split(";")
            game_data = [[0] * len(sets) for _ in range(3)]
            for i, s in enumerate(sets):
                moves = [
                    tuple(move.strip().split(" "))
                    for move in s.strip().split(",")
                ]
                for move in moves:
                    game_data[int(move[1])][i] += int(move[0])
            games[game] = game_data
        return games

    @staticmethod
    def _check_moves(draws: list[int], maximum: int) -> bool:
        """Check if the draws in a game are within the maximum limits.

        Args:
            draws (list[int]): The draws made in a game.
            maximum (int): The maximum limit for a draw.

        Returns:
            bool: True if all draws are within the maximum limit, False otherwise.
        """
        return not any(draw > maximum for draw in draws)

    def _check_games(self, maximum: list[int, int, int]) -> dict:
        """Check the games and return a dictionary of valid games.

        Args:
            maximum (list[int, int, int]): The maximum limits for each draw.

        Returns:
            dict: A dictionary containing valid games.
                  The keys are game numbers and the values is a list with a
                  list for each cube color representing the moves made in each
                  game for that color.
        """
        return dict(
            filter(
                lambda item: all(
                    [self._check_moves(x, y) for x, y in zip(item[1], maximum)]
                ),
                self.data.items(),
            )
        )

    def part_1(self, maximum: list[int, int, int]) -> int:
        """Calculate the sum of game numbers for valid games.

        Args:
            maximum (list[int, int, int]): The maximum limits for each draw.

        Returns:
            int: The sum of game numbers for valid games.
        """
        return sum(self._check_games(maximum).keys())

    def _mvg(self, game: list[list[int]]) -> list[int]:
        """Calculate the Minimum Viable Game (MVG)
        Calculates the minimum cubes needed for each color to
          have a valid game.
        Args:
            game (list[list[int]]): The moves made in a game.

        Returns:
            list[int]: The minimum cubes needed to have a valid game.
        """
        return [max(x) for x in game]

    def part_2(self) -> int:
        """Calculates the sum of MVG products for all games.

        Returns:
            int: The product of the maximum draws in each game.
        """
        return sum(
            [
                reduce(lambda x, y: x * y, self._mvg(sets))
                for _, sets in self.data.items()
            ]
        )


if __name__ == "__main__":
    d2 = Day2("./input/day_2.txt")
    print(f"Part 1: {d2.part_1([12,13,14])}")
    print(f"Part 2: {d2.part_2()}")
