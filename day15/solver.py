import sys
import numpy as np
from collections import defaultdict

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    # return [list(map(int, line)) for line in raw_data.splitlines()]
    graph = {}
    for y, line in enumerate(raw_data.splitlines()):
        for x, v in enumerate(line):
            graph[(x, y)] = int(v)
    return graph


def dijkstra(start, dest, grid):
    unvisited = set(grid.keys())
    visited = set()
    distances = {p: np.inf for p in unvisited}
    distances[start] = 0
    while unvisited:
        current_candidates = {p: d for p,d in distances.items() if p in unvisited}
        current = min(current_candidates, key=current_candidates.get)
        x, y = current
        neighbors = [(x, y+1), (x, y-1),
                     (x+1, y), (x-1, y)]
        for n in neighbors:
            if n in visited or n not in grid:
                continue
            distance = distances[current] + grid[n]
            if distance < distances[n]:
                distances[n] = distance
        unvisited.remove(current)
        visited.add(current)
    return distances[dest]


# PART 1
@measure_time
def solve1(data):
    target = max(data)
    return dijkstra((0, 0), target, data)


def wrap(a, b):
    if a + b < 10:
        return a+b
    else:
        return (a+b) % 10 + 1

# PART 2
@measure_time
def solve2(data):
    xm, ym = max(data)
    xdim, ydim = xm+1, ym+1
    for (x, y) in list(data.keys()):
        for i in range(5):
            for j in range(5):
                if (i, j) in [(0,0), (0, 3), (0, 4), (1, 4), (3, 0), (4, 0), (4, 1)]:
                    continue
                if i == 0 and j == 0:
                    continue
                data[(x + xdim*j, y + ydim*i)] = wrap(data[(x, y)], i+j)
    target = max(data)
    return dijkstra((0, 0), target, data)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

