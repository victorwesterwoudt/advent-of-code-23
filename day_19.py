from __future__ import annotations
from src import Day
from functools import cached_property
from collections import deque
import math


class Part(object):
    def __init__(self, part: str) -> None:
        self._part = part
        self.x, self.m, self.a, self.s = [
            int(x.split("=")[1]) for x in part.strip("\{\}").split(",")
        ]

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __repr__(self) -> str:
        return f"x: {self.x}, m: {self.m}, a: {self.a}, s: {self.s}"

    @property
    def score(self):
        return self.x + self.m + self.a + self.s


class Workflow(object):
    def __init__(self, key: str, workflow: str, fdict) -> None:
        self._workflow = workflow.strip("\{\}").split(",")
        self.fdict = fdict
        if key == "A":
            self._fs = [self.A]
        elif key == "R":
            self._fs = [self.R]
        else:
            self._fs = [self.str_to_lambda(s, fdict) for s in self._workflow]

    @property
    def workflow(self):
        return [self._split(s) for s in self._workflow]

    def __call__(self, x):
        for f in self._fs:
            y = f(x)
            if y >= 0:
                return y
        return False

    def R(self, x):
        return 0

    def A(self, x):
        return 1

    @staticmethod
    def _split(s: str):
        if ":" in s:
            key, operator = s[:2]
            value, output = s[2:].split(":")
            value = int(value)
        else:
            key, operator, value = None, None, None
            output = s
        return key, operator, value, output

    def str_to_lambda(self, s, functions: dict[str, Workflow]):
        key, operator, value, output = self._split(s)
        if key:
            if operator == "<":

                def f(x):
                    if x[key] < value:
                        return functions[output](x)
                    else:
                        return -1

            else:

                def f(x):
                    if x[key] > value:
                        return functions[output](x)
                    else:
                        return -1

        else:

            def f(x):
                return functions[s](x)

        return f


class Day19(Day):
    @cached_property
    def data(self):
        output = [[], []]
        i = 0
        for line in self.raw_data:
            if line == "":
                i += 1
            else:
                output[i].append(line)

        parts = []
        for p in output[1]:
            parts.append(Part(p))

        workflows = {}
        for line in output[0]:
            key, workflow = line.strip("\{\}").split("{")
            workflows[key] = workflow

        return workflows, parts

    @property
    def parts(self) -> list[Part]:
        return self.data[1]

    @cached_property
    def workflows(self) -> dict[str, Workflow]:
        functions = {}
        workflows = self.data[0]
        for k, v in workflows.items():
            functions[k] = Workflow(k, v, functions)

        functions["A"] = Workflow("A", "", functions)
        functions["R"] = Workflow("R", "", functions)
        return functions

    def split_ranges(
        self, ranges: dict[str, range], key: str, at: int, operator: str
    ):
        output = [{}, {}]
        if operator == "<":
            at -= 1
        for k, v in ranges.items():
            if k == key:
                if at < v.start:
                    output[0][k] = range(v.start, v.start)
                    output[1][k] = range(v.start, v.stop)
                elif at > v.stop:
                    output[0][k] = range(v.start, v.stop)
                    output[1][k] = range(v.stop, v.stop)
                else:
                    output[0][k] = range(v.start, min(v.stop, at))
                    output[1][k] = range(max(v.start, at), v.stop)
            else:
                output[0][k], output[1][k] = v, v
        return output

    def part1(self):
        ans = 0
        for p in self.parts:
            if self.workflows["in"](p):
                ans += p.score
        return ans

    def part2(self):
        queue = deque(
            [
                (
                    "in",
                    {
                        "x": range(0, 4000),
                        "m": range(0, 4000),
                        "a": range(0, 4000),
                        "s": range(0, 4000),
                    },
                )
            ]
        )

        score = 0

        while queue:
            key, ranges = queue.popleft()
            wf = self.workflows[key].workflow

            if key == "A":
                score += math.prod([len(v) for v in ranges.values()])
                continue
            elif key == "R":
                continue

            for k, operator, value, output in wf:
                if operator:
                    before, after = self.split_ranges(
                        ranges, k, value, operator
                    )
                    if operator == "<":
                        queue.append((output, before))
                        ranges = after
                    else:
                        ranges = before
                        queue.append((output, after))
                else:
                    queue.append((output, ranges))

        return score


if __name__ == "__main__":
    d = Day19("./input/day_19.txt")
    print(f"Part 1: {d.part1()}")
    print(f"Part 2: {d.part2()}")
