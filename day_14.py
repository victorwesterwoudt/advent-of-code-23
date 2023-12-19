from src import Day
from functools import cached_property
from collections import deque
from hashlib import sha1


class Day14(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            output.append(tuple([x for x in line]))
        return output

    @staticmethod
    def transpose(array: list[list[str]]):
        return [list(i) for i in zip(*array)]

    @classmethod
    def tilt(cls, array: list[list[str]], flip=False):
        if flip:
            return tuple([cls._sort(x[::-1])[::-1] for x in array])
        else:
            return tuple([cls._sort(x) for x in array])

    @staticmethod
    def _sort(line):
        q = deque(line)
        s = deque()
        t = deque()
        while q:
            i = q.popleft()
            if i == "O":
                s.append(i)
            elif i == ".":
                t.append(i)
            else:
                s.extend(t)
                t = deque()
                s.append(i)
        if t:
            s.extend(t)
        return tuple(s)

    @classmethod
    def north(cls, array):
        return cls.transpose(cls.tilt(cls.transpose(array)))

    @classmethod
    def west(cls, array):
        return cls.tilt(array)

    @classmethod
    def east(cls, array):
        return cls.tilt(array, flip=True)

    @classmethod
    def south(cls, array):
        return cls.transpose(cls.tilt(cls.transpose(array), flip=True))

    @classmethod
    def weight(cls, array):
        T = cls.transpose(array)
        ans = 0
        for row in T:
            ans += sum([len(row) - i for i, x in enumerate(row) if x == "O"])

        return ans

    @classmethod
    def cycle(cls, array):
        output = cls.east(cls.south(cls.west(cls.north(array))))
        h = str(hash(output))
        w = cls.weight(output)

        return output, sha1(h.encode("utf-8")).hexdigest(), w

    def part_1(self):
        return self.weight(self.north(self.data))

    def part_2(self):
        hashes = {}
        array = self.data
        i = 1
        while True:
            array, h, w = self.cycle(array)
            if h in hashes:
                break
            else:
                hashes[h] = (i, w)
                i += 1

        N = 1000000000
        n = (N - hashes[h][0]) % (i - hashes[h][0]) + hashes[h][0]
        return [x[1] for x in hashes.values() if x[0] == n][0]


if __name__ == "__main__":
    d = Day14("./input/day_14.txt")
    print("Part 1:", d.part_1())
    print("Part 2:", d.part_2())
