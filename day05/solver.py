import sys
import numpy as np

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    points = []
    for line in raw_data.splitlines():
        start, end = line.split(" -> ")
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")
        points.append(((int(x1), int(y1)), (int(x2), int(y2))))
    return points


def create_linegrid(points):
    edge = (
        max(max(p1[0], p2[0]) for p1, p2 in points) + 1,
        max(max(p1[1], p2[1]) for p1, p2 in points) + 1
    )
    # print(edge)
    grid = [
        [0 for _ in range(edge[0])]
        for _ in range(edge[1])
    ]
    for p1, p2 in points:
        dx = np.sign(p2[0] - p1[0])
        dy = np.sign(p2[1] - p1[1])
        # print(f"{dx=}{dy=}")
        current = p1
        while current != p2:
            # print(current)
            grid[current[1]][current[0]] += 1
            current = (current[0] + dx, current[1] + dy)
            if dx == dy == 0:
                return grid
        # add last point
        grid[current[1]][current[0]] += 1
    return grid


# PART 1
@measure_time
def solve1(data):
    # take only horizontal or vertical lines
    data = list(filter(lambda ps: ps[0][0]==ps[1][0] or ps[0][1]==ps[1][1], data))
    grid = create_linegrid(data)
    count = 0
    for line in grid:
        # print(line)
        for c in line:
            if c > 1:
                count += 1
    return count


# PART 2
@measure_time
def solve2(data):
    grid = create_linegrid(data)
    count = 0
    for line in grid:
        # print(line)
        for c in line:
            if c > 1:
                count += 1
    return count


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

