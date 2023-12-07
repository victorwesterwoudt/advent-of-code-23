from src import Day


class Day5(Day):
    """
    A class representing the solution for Day 5 of the Advent
    of Code challenge.
    """

    @property
    def seeds(self):
        return [int(x) for x in self.data[0].split(":")[1].split()]

    @property
    def blocks(self):
        blocks = []
        for line in d.data[2:]:
            if ":" in line:
                blocks.append([])
            else:
                if v := [int(x) for x in line.split()]:
                    blocks[-1].append(v)
        return blocks

    def part_1(self):
        soils = []
        for seed in self.seeds:
            for block in self.blocks:
                for dest, src, sz in block:
                    if seed in range(src, src + sz):
                        seed = dest + (seed - src)
                        break
            soils.append(seed)
        return min(soils)

    def rsolve(
        self,
        source_ranges: list[tuple[int, int]],
        block: list[list[int, int, int]],
    ) -> list[tuple[int, int]]:
        """
        Resolve the destination ranges based on the source ranges and blocks.

        Args:
            SR: A list of tuples representing the source ranges.
            block: A list of lists representing the mappings from source
                to dest for a stage in the seed to soil map.

        Returns:
            A list of tuples representing the destination ranges.
        """
        # destination ranges
        dest_ranges = []
        for dest, src, sz in block:
            # intermediate ranges
            inter_ranges = []
            while source_ranges:
                start, stop = source_ranges.pop()

                # split intervals
                pre = (start, min(src, stop))
                overlap = (max(start, src), min(src + sz, stop))
                post = (max(src + sz, start), stop)

                if pre[1] > pre[0]:
                    inter_ranges.append((pre[0], pre[1]))
                if overlap[1] > overlap[0]:
                    dest_ranges.append(
                        (dest + (overlap[0] - src), dest + (overlap[1] - src))
                    )
                if post[1] > post[0]:
                    inter_ranges.append((post[0], post[1]))
            source_ranges = inter_ranges
        return dest_ranges + source_ranges

    def part_2(self):
        seeds = [tuple(x) for x in zip(self.seeds[::2], self.seeds[1::2])]
        seeds = [[(start, start + size)] for start, size in seeds]
        soils = []
        for seed in seeds:
            for block in self.blocks:
                seed = self.rsolve(seed, block)

            soils.append(min(seed, key=lambda x: x[0]))

        return min(soils, key=lambda x: x[0])[0]


if __name__ == "__main__":
    d = Day5("./input/day_5.txt")
    print(d.part_1())
    print(d.part_2())
