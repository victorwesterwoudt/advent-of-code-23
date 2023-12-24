from __future__ import annotations
from src import Day
from functools import cached_property, lru_cache
from enum import Enum
import heapq as hq


class Direction(Enum):
    delta: tuple[int, int]

    def __new__(cls, value, delta):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.delta = delta
        return obj

    def __lt__(self, other: "Direction"):
        return self.value < other.value

    @cached_property
    def opposite(self):
        return Direction((self.value + 2) % 4)

    def __repr__(self):
        return f"Direction.{self.name}"

    NORTH = (0, (-1, 0))
    EAST = (1, (0, 1))
    SOUTH = (2, (1, 0))
    WEST = (3, (0, -1))


class Graph:
    EDGES = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, map: list[str]) -> None:
        self._map = []
        for line in map:
            self._map.append([int(x) for x in line])

    def __getitem__(self, key: tuple[int, int]) -> int:
        r, c = key
        return self._map[r][c]

    @cached_property
    def width(self) -> int:
        return len(self._map[0])

    @cached_property
    def height(self) -> int:
        return len(self._map)

    @lru_cache(maxsize=None)
    def edges(
        self, rc: tuple[int, int]
    ) -> dict[tuple[int, int], tuple[int, Direction]]:
        r, c = rc
        output = {}
        for d in Direction:
            dr, dc = d.delta
            if (r + dr) < 0 or (c + dc) < 0:
                continue
            elif (r + dr) >= self.height or (c + dc) >= self.width:
                continue
            output[(r + dr, c + dc)] = (self[r + dr, c + dc], d)
        return output

    def next(
        self, rc: tuple[int, int], direction: Direction
    ) -> tuple[int, int]:
        dr, dc = direction.delta
        r, c = rc

        if r + dr < 0 or c + dc < 0:
            raise ValueError("Out of bounds")
        elif r + dr >= self.height or c + dc >= self.width:
            raise ValueError("Out of bounds")

        return ((r + dr, c + dc), self[r + dr, c + dc])

    def show_route(self, route: list[tuple[int, int]]) -> None:
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in route:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def dijkstra(
        self,
        root: tuple[int, int],
        destination: tuple[int, int],
        part_2: bool = False,
    ):
        weight = {}
        weight[root, ()] = (0, None)

        queue = []
        hq.heappush(queue, (0, root, ()))

        while queue:
            w, node, direction = hq.heappop(queue)

            edges = self.edges(node)

            for n, (wn, d) in edges.items():
                if direction and d.opposite == direction[0]:
                    continue

                _dir = (
                    d,
                    direction[1] + 1 if direction and d == direction[0] else 1,
                )

                if part_2 and _dir[1] == 1:
                    try:
                        for _ in range(3):
                            _n, _w = self.next(n, d)
                            wn += _w
                            n = _n
                            _dir = (_dir[0], _dir[1] + 1)
                    except ValueError:
                        continue

                if _dir[1] > (3 if not part_2 else 10):
                    continue

                if (n, _dir) not in weight or weight[(n, _dir)][0] > w + wn:
                    weight[(n, _dir)] = (w + wn, node)
                    hq.heappush(queue, (w + wn, n, _dir))

        return weight, min(
            [v[0] for k, v in weight.items() if k[0] == destination]
        )


class Day17(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            output.append([int(x) for x in line])
        return output

    @cached_property
    def graph(self) -> Graph:
        return Graph(self.data)

    def part_1(self):
        _, ans = self.graph.dijkstra(
            (0, 0), (self.graph.height - 1, self.graph.width - 1)
        )
        return ans

    def part_2(self):
        _, ans = self.graph.dijkstra(
            (0, 0), (self.graph.height - 1, self.graph.width - 1), part_2=True
        )
        return ans


if __name__ == "__main__":
    d = Day17("./input/day_17.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
