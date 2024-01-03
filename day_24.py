from src import Day
import sympy


class Hailstone:
    def __init__(self, definition):
        self._definition = definition
        loc, v = definition.split("@")
        self.x, self.y, self.z = tuple(
            [int(x.strip()) for x in loc.split(",")]
        )
        self.vx, self.vy, self.vz = tuple(
            [int(x.strip()) for x in v.split(",")]
        )

        self.a = self.vy
        self.b = -self.vx
        self.c = self.vy * self.x - self.vx * self.y

    def __repr__(self):
        return f"Hailstone({self._definition})"

    def intersects(
        self,
        other: "Hailstone",
        bounds: tuple = (200000000000000, 400000000000000),
    ):
        if self.a * other.b == other.a * self.b:
            return False

        denominator = self.a * other.b - other.a * self.b

        x = (self.c * other.b - other.c * self.b) / denominator
        y = (other.c * self.a - self.c * other.a) / denominator

        if (
            (x - self.x) * self.vx < 0
            or (y - self.y) * self.vy < 0
            or (x - other.x) * other.vx < 0
            or (y - other.y) * other.vy < 0
        ):
            return False

        if bounds[0] <= x <= bounds[1] and bounds[0] <= y <= bounds[1]:
            return True


class Day24(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hailstones = [Hailstone(h) for h in self.raw_data]

    def part_1(self):
        ans = 0

        for i, hs in enumerate(self.hailstones):
            for h in self.hailstones[:i]:
                if a := hs.intersects(h):
                    ans += a

        return ans

    def part_2(self):
        xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr yr zr vxr vyr vzr")
        equations = []

        for i, h in enumerate(self.hailstones):
            x, y, z = h.x, h.y, h.z
            vx, vy, vz = h.vx, h.vy, h.vz

            equations.append((xr - x) * (vy - vyr) - (yr - y) * (vx - vxr))
            equations.append((xr - x) * (vz - vzr) - (zr - z) * (vx - vxr))

            # assuming there is 1 answer, we need at least 3 hailstones to find it
            if i < 2:
                continue

            answers = [
                sol
                for sol in sympy.solve(equations)
                if all(x % 1 == 0 for x in sol.values())
            ]

            if len(answers) == 1:
                break

        return answers[0][xr] + answers[0][yr] + answers[0][zr]


if __name__ == "__main__":
    d = Day24("./input/day_24.txt")

    print("Part 1:", d.part_1())
    print("Part 2:", d.part_2())
