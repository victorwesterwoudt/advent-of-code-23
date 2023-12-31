from src import Day
from functools import cached_property
from collections import deque


class Map:
    def __init__(self, data: list[str]):
        self._data = data
        self._nb_cache = {}

    @cached_property
    def map(self):
        output: list[list] = []
        for line in self._data:
            output.append([])
            for char in line:
                output[-1].append("." if char == "S" else char)

        return output

    @cached_property
    def width(self):
        return len(self.map[0])

    @cached_property
    def height(self):
        return len(self.map)

    @cached_property
    def start(self):
        for r, line in enumerate(self._data):
            for c, char in enumerate(line):
                if char == "S":
                    return (r, c)

    def __getitem__(self, rc: tuple[int, int]):
        # this makes the map infinitely accessible
        rc = (rc[0] % self.height, rc[1] % self.width)
        return self.map[rc[0]][rc[1]]

    def BFS(self, n, sr=None, sc=None, inside=True):
        if sr is None:
            sr = self.start[0]

        if sc is None:
            sc = self.start[1]

        w, h = self.width, self.height
        ans = set()
        seen = {(sr, sc)}
        q = deque([(sr, sc, n)])

        while q:
            r, c, s = q.popleft()

            if s % 2 == 0:
                ans.add((r, c))
            if s == 0:
                continue

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if inside:
                    if nr < 0 or nr >= h or nc < 0 or nc >= w:
                        continue
                if self[(nr, nc)] == "#":
                    continue
                if (nr, nc) in seen:
                    continue
                seen.add((nr, nc))
                q.append((nr, nc, s - 1))

        return ans

    def show(self, bfs):
        r_min, r_max = min([x[0] for x in bfs]), max([x[0] for x in bfs])
        c_min, c_max = min([x[1] for x in bfs]), max([x[1] for x in bfs])
        temp = [
            [self[(r, c)] for c in range(c_min, c_max + 1)]
            for r in range(r_min, r_max + 1)
        ]
        bfs_corrected = [(r - r_min, c - c_min) for r, c in bfs]

        for r, c in bfs_corrected:
            temp[r][c] = "O"

        for line in temp:
            print("".join(line))


class Day21(Day):
    def __init__(self, input_file_path: str):
        super().__init__(input_file_path)
        self.map = Map(self.raw_data)

    def part_1(self):
        return len(d.map.BFS(64))

    def part_2(self):
        steps = 26501365
        w, h = self.map.width, self.map.height
        sr, sc = self.map.start
        radius = steps // w

        c_starts = [(h - 1, 0), (0, 0), (0, w - 1), (h - 1, w - 1)]

        small = [self.map.BFS(w // 2 - 1, r, c) for r, c in c_starts]
        large = [self.map.BFS(w + w // 2 - 1, r, c) for r, c in c_starts]

        t_starts = [(h - 1, sc), (0, sc), (sr, 0), (sr, w - 1)]
        corners = [self.map.BFS(w - 1, r, c) for r, c in t_starts]

        u = self.map.BFS(w + w // 2 + (0 if steps % 2 != 0 else 1), sr, sc)
        e = self.map.BFS(w + w // 2 + (1 if steps % 2 != 0 else 0), sr, sc)

        return (
            self.floor_odd(radius) ** 2 * len(e)
            + self.floor_even(radius) ** 2 * len(u)
            + sum([(radius - 1) * len(x) for x in large])
            + sum([radius * len(x) for x in small])
            + sum([len(x) for x in corners])
        )

    def floor_odd(self, n):
        if n % 2 == 0:
            return n - 1
        else:
            return n

    def floor_even(self, n):
        if n % 2 == 1:
            return n - 1
        else:
            return n


if __name__ == "__main__":
    d = Day21("./input/day_21.txt")
    print(f"Part 1: {d.part_1()}")
    print(f"Part 2: {d.part_2()}")
