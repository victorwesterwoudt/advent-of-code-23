from __future__ import annotations
from src import Day
from functools import cached_property
from enum import Enum


class Direction(Enum):
    d: str
    delta: tuple[int, int]

    def __new__(cls, value, d, delta):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.d = d
        obj.delta = delta
        return obj

    def next(self, coordinate):
        return tuple([x + y for x, y in zip(coordinate, self.delta)])

    NORTH = (0, "n", (-1, 0))
    EAST = (1, "e", (0, 1))
    SOUTH = (2, "s", (1, 0))
    WEST = (3, "w", (0, -1))


class Map(object):
    def __init__(self, map: list[list[str]]) -> None:
        self._map = map

    @property
    def width(self):
        return len(self._map[0])

    @property
    def height(self):
        return len(self._map)

    @cached_property
    def map(self):
        map = {}
        for i, line in enumerate(self._map):
            for j, element in enumerate(line):
                if element != ".":
                    map[i, j] = Element(element)

        return map

    def energized(self, beams: list[Beam]):
        energized = set()
        for beam in beams:
            energized = energized | set(beam.energized)

        energized = set(
            filter(
                lambda x: x[0] >= 0
                and x[1] >= 0
                and x[0] < self.height
                and x[1] < self.width,
                energized,
            )
        )

        return energized, len(energized)

    def solve(self, beam: Beam):
        beams = []
        open_beams = [beam]
        exits = []

        while open_beams:
            beam = open_beams.pop(0)
            _, new_beams = beam.shine(self)

            if beam in beams:
                continue
            else:
                beams.append(beam)

            if not new_beams and beam.exits(self):
                exits.append(beam)
            else:
                open_beams.extend(
                    list(filter(lambda x: x not in beams, new_beams))
                )

        _, energy = self.energized(beams)

        return energy, exits


class Beam(object):
    def __init__(self, start: tuple[int, int], direction=Direction.EAST):
        self.start = start
        self.direction = direction
        self.end = direction.next(start)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}: {self.start}"
            f" -> {self.end} ({self.direction}))"
        )

    def __eq__(self, o: object) -> bool:
        return self.start == o.start and self.end == o.end

    def _shine(self):
        coord = self.end
        while True:
            yield coord
            coord = self.direction.next(coord)

    def shine(self, map: Map) -> tuple["Beam", tuple["Beam", ...]]:
        f = self._shine()
        p = self.end
        while True:
            n = next(f)
            if n in map.map:
                self.end = n
                d = map.map[n].hit[self.direction]
                if isinstance(d, Direction):
                    beams = tuple([Beam(n, d)])
                else:
                    beams = tuple([Beam(n, x) for x in d])
                return self, tuple(
                    filter(
                        lambda x: not (
                            x.end[0] < 0
                            or x.end[0] >= len(map._map)
                            or x.end[1] < 0
                            or x.end[1] >= len(map._map[0])
                        ),
                        beams,
                    )
                )
            elif (
                n[0] < 0
                or n[0] >= len(map._map)
                or n[1] < 0
                or n[1] >= len(map._map[0])
            ):
                self.end = p
                return self, tuple([])

            p = n

    @property
    def energized(self) -> list[tuple[int, int]]:
        a, b = sorted((self.start, self.end))
        if a[0] == b[0]:
            return [(a[0], c) for c in range(a[1], b[1] + 1)]
        else:
            return [(r, a[1]) for r in range(a[0], b[0] + 1)]

    def exits(self, map: Map):
        if map._map[self.end[0]][self.end[1]] != ".":
            return False

        match self.direction:
            case Direction.NORTH:
                return self.end[0] <= 0
            case Direction.SOUTH:
                return self.end[0] >= (map.height - 1)
            case Direction.WEST:
                return self.end[1] <= 0
            case Direction.EAST:
                return self.end[1] >= (map.width - 1)

    def to_entrance(self, map: Map):
        if self.exits(map):
            match self.direction:
                case Direction.NORTH:
                    return Beam((-1, self.end[1]), Direction.SOUTH)
                case Direction.SOUTH:
                    return Beam((map.height, self.end[1]), Direction.NORTH)
                case Direction.EAST:
                    return Beam((self.end[0], map.width), Direction.WEST)
                case Direction.WEST:
                    return Beam((self.end[0], -1), Direction.EAST)
        else:
            raise ValueError("Beam is not an exit")


class Element(Enum):
    hit: dict[Direction, Direction | tuple[Direction, Direction]]

    def __new__(
        cls,
        value: str,
        hit: dict[Direction, Direction | tuple[Direction, Direction]],
    ):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.hit = hit
        return obj

    BACKSLASH = (
        "\\",
        {
            Direction.EAST: Direction.SOUTH,
            Direction.WEST: Direction.NORTH,
            Direction.NORTH: Direction.WEST,
            Direction.SOUTH: Direction.EAST,
        },
    )
    SLASH = (
        "/",
        {
            Direction.EAST: Direction.NORTH,
            Direction.WEST: Direction.SOUTH,
            Direction.NORTH: Direction.EAST,
            Direction.SOUTH: Direction.WEST,
        },
    )
    VBAR = (
        "|",
        {
            Direction.EAST: (Direction.NORTH, Direction.SOUTH),
            Direction.WEST: (Direction.NORTH, Direction.SOUTH),
            Direction.NORTH: Direction.NORTH,
            Direction.SOUTH: Direction.SOUTH,
        },
    )
    BAR = (
        "-",
        {
            Direction.EAST: Direction.EAST,
            Direction.WEST: Direction.WEST,
            Direction.SOUTH: (Direction.EAST, Direction.WEST),
            Direction.NORTH: (Direction.EAST, Direction.WEST),
        },
    )


class Day16(Day):
    @cached_property
    def data(self):
        map = []
        for line in self.raw_data:
            map.append([x for x in line])
        return Map(map)

    def part_1(self):
        output, _ = self.data.solve(Beam((0, -1)))
        return output

    def part_2(self):
        entrances = {}

        assert self.data.height == self.data.width

        for i in range(self.data.height):
            beams = [
                Beam((i, -1), Direction.EAST),
                Beam((i, self.data.width), Direction.WEST),
                Beam((-1, i), Direction.SOUTH),
                Beam((self.data.height, i), Direction.NORTH),
            ]

            for b in beams:
                if b.start in entrances:
                    continue

                energy, exits = self.data.solve(b)
                entrances[b.start] = energy
                newes = [ex.to_entrance(self.data) for ex in exits]
                for new in newes:
                    entrances[new.start] = energy

            if i % 10 == 0:
                print(f"iteration: {i}, covered: {len(entrances)} entrances")

        return max(entrances.values())


if __name__ == "__main__":
    d = Day16("./input/day_16.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
