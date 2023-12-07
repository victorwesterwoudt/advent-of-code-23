from src import Day

if __name__ == "__main__":
    d3 = Day("./input/day_3.txt")

    w = len(d3.data[0])
    h = len(d3.data)

    part = ["", None]
    parts = []
    ispart = False

    for r, line in enumerate(d3.data):
        for c, char in enumerate(line):
            if not char.isdigit():
                if part[0] != "" and ispart:
                    part[0] = int(part[0])
                    parts.append(part)
                part = ["", None]
                ispart = False
            elif char.isdigit():
                part[0] += char

                for ln in range(max(0, r - 1), min(h, r + 2)):
                    for x in range(max(0, c - 1), min(w, c + 2)):
                        if (
                            not d3.data[ln][x].isnumeric()
                            and d3.data[ln][x] != "."
                        ):
                            ispart = True
                            part[1] = (ln, x, d3.data[ln][x])

    stars = [x[1] for x in parts if x[1][2] == "*"]
    stars = set([star for star in stars if stars.count(star) == 2])

    gr = 0
    for star in stars:
        gears = list(filter(lambda x: x[1] == star, parts))
        gr += gears[0][0] * gears[1][0]

    print(f"Part 1: {sum([x[0] for x in parts])}")
    print(f"Part 2: {gr}")
