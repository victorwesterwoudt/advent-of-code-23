from src import Day
from functools import cached_property


class Day13(Day):
    @cached_property
    def data(self):
        maps = [[]]
        for line in self.raw_data:
            if line == "":
                maps.append([])
            else:
                maps[-1].append(line)
        return maps

    def map(self, idx, transposed=False):
        if transposed:
            return ["".join(x) for x in zip(*self.data[idx])]
        else:
            return self.data[idx]

    def _reflect(self, mp, dist=0):
        i = 0
        while i < len(mp) - 1:
            i += 1
            am = mp[:i]
            pm = mp[i:]
            n = min(len(am), len(pm))
            if (
                sum(
                    [
                        x != y
                        for x, y in zip("".join(am[::-1][:n]), "".join(pm[:n]))
                    ]
                )
                == dist
            ):
                return i

        return False

    def reflection(self, idx, dist=0):
        score = 0
        for T in [False, True]:
            n = self._reflect(self.map(idx, T), dist=dist)
            score += n if T else n * 100
        return score

    def part_1(self):
        ans = 0
        for i in range(len(self.data)):
            ans += d.reflection(i, dist=0)
        return ans

    def part_2(self):
        ans = 0
        for i in range(len(self.data)):
            ans += d.reflection(i, dist=1)
        return ans


if __name__ == "__main__":
    d = Day13("./input/day_13.txt")
    print("Part 1:", d.part_1())
    print("Part 2:", d.part_2())
