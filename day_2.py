from src import Day
from functools import reduce


class Day2(Day):
    @property
    def data(self) -> dict:
        games = {}
        for line in self.raw_data:
            line = line.replace("red", "0").replace("blue", "2").replace("green", "1")
            game, sets = line.split(":")
            game = int(game.strip().replace("Game ", ""))
            sets = sets.split(";")
            game_data = [[0] * len(sets) for _ in range(3)]
            for i, s in enumerate(sets):
                moves = [tuple(move.strip().split(" ")) for move in s.strip().split(",")]
                for move in moves:
                    game_data[int(move[1])][i] += int(move[0])
            games[game] = game_data
        return games

    @staticmethod
    def _check_moves(draws: list[int], maximum: int) -> bool:
        return not any(draw > maximum for draw in draws)

    def _check_games(self, maximum: list[int, int, int]) -> dict:
        return dict(
            filter(
                lambda item: all(
                    [self._check_moves(x, y) for x, y in zip(item[1], maximum)]
                ),
                self.data.items(),
            )
        )

    def part_1(self, maximum: list[int, int, int]) -> int:
        return sum(self._check_games(maximum).keys())

    def part_2(self) -> int:
        return sum(
            [
                reduce(lambda x, y: x * y, [max(s) for s in sets])
                for _, sets in self.data.items()
            ]
        )


if __name__ == "__main__":
    d2 = Day2("./input/day_2.txt")
    print(f"Part 1: {d2.part_1([12,13,14])}")
    print(f"Part 2: {d2.part_2()}")
