from src import Day
from functools import cached_property, reduce
from collections import defaultdict
import re


class Day15(Day):
    @cached_property
    def data(self):
        output = []
        for line in self.raw_data:
            output.extend(line.split(","))
        return output

    @property
    def boxes(self):
        boxes = defaultdict(lambda: {"labels": [], "focals": []})
        for instruction in self.data:
            label, op, fl = re.split("([=-])", instruction)
            box = boxes[hash(label)]

            if op == "=":
                if label in box["labels"]:
                    idx = box["labels"].index(label)
                    box["focals"][idx] = int(fl)
                else:
                    box["labels"].append(label)
                    box["focals"].append(int(fl))
            elif op == "-":
                if label in box["labels"]:
                    idx = box["labels"].index(label)
                    del box["labels"][idx]
                    del box["focals"][idx]
            else:
                continue
        return boxes

    def part_1(self):
        ans = 0
        for d in self.data:
            ans += hash(d)
        return ans

    def part_2(self):
        ans = 0
        for i, box in self.boxes.items():
            ans += sum(
                [(i + 1) * (x + 1) * y for x, y in enumerate(box["focals"])]
            )

        return ans


def _hash(x, y):
    return (x + ord(y)) * 17 % 256


def hash(s: str):
    return reduce(_hash, s, 0)


if __name__ == "__main__":
    d = Day15("./input/day_15.txt")
    print("Part 1:", d.part_1())
    print("Part 2:", d.part_2())
