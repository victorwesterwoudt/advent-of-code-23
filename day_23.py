from src import Day
from functools import cached_property


class Day23(Day):
    DIRS = {
        "<": [(0, -1)],
        ">": [(0, 1)],
        "^": [(-1, 0)],
        "v": [(1, 0)],
        ".": [(0, -1), (0, 1), (-1, 0), (1, 0)],
    }

    @cached_property
    def data(self):
        return self.raw_data

    @cached_property
    def width(self):
        return len(self.data[0])

    @cached_property
    def height(self):
        return len(self.data)

    @cached_property
    def start(self):
        return (0, self.data[0].index("."))

    @cached_property
    def end(self):
        return (len(self.data) - 1, self.data[-1].index("."))

    def calculate_graph(self, allowed_directions=DIRS):
        nodes = [self.start, self.end]
        for r, row in enumerate(self.data):
            for c, ch in enumerate(row):
                if ch == "#":
                    continue
                neighbours = 0
                for nr, nc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (
                        0 <= r + nr < self.height
                        and 0 <= c + nc < self.width
                        and self.data[r + nr][c + nc] != "#"
                    ):
                        neighbours += 1
                if neighbours >= 3:
                    nodes.append((r, c))

        graph = {node: {} for node in nodes}

        for node in nodes:
            stack = [(node, 0)]
            seen = set([node])

            while stack:
                (r, c), n = stack.pop()

                if (r, c) in nodes and (r, c) != node:
                    graph[node][(r, c)] = n
                    continue

                for dr, dc in allowed_directions[self.data[r][c]]:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < self.height
                        and 0 <= nc < self.width
                        and self.data[nr][nc] != "#"
                        and (nr, nc) not in seen
                    ):
                        stack.append(((nr, nc), n + 1))
                        seen.add((nr, nc))

        return graph

    def DFS(self, graph, node: tuple[int, int] = None, visited: set = set()):
        if not node:
            node = self.start

        if node == self.end:
            return 0

        m = -float("inf")
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                m = max(
                    m,
                    self.DFS(graph, neighbor, visited) + graph[node][neighbor],
                )

        visited.remove(node)

        return m

    def part1(self) -> int:
        graph = self.calculate_graph()
        return self.DFS(graph)

    def part2(self) -> int:
        newdirs = {
            "<": [(0, -1), (0, 1), (-1, 0), (1, 0)],
            ">": [(0, -1), (0, 1), (-1, 0), (1, 0)],
            "^": [(0, -1), (0, 1), (-1, 0), (1, 0)],
            "v": [(0, -1), (0, 1), (-1, 0), (1, 0)],
            ".": [(0, -1), (0, 1), (-1, 0), (1, 0)],
        }
        graph = self.calculate_graph(newdirs)
        return self.DFS(graph)


if __name__ == "__main__":
    d = Day23("./input/day_23.txt")
    print(f"Part 1: {d.part1()}")
    print(f"Part 2: {d.part2()}")
