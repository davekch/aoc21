import sys
import numpy as np
from collections import defaultdict

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [list(map(int, line)) for line in raw_data.splitlines()]
    # graph = {}
    # for y, line in enumerate(raw_data.splitlines()):
    #     for x, v in enumerate(line):
    #         graph[(x, y)] = int(v)
    # return graph


def dijkstra(start, dest, grid):
    xdim, ydim = len(grid[0]), len(grid)
    unvisited = set((x, y) for x in range(xdim) for y in range(ydim))
    visited = set()
    paths = defaultdict(list)
    distances = {p: np.inf for p in unvisited}
    distances[start] = 0
    while unvisited:
        current_candidates = {p: d for p,d in distances.items() if p in unvisited}
        current = min(current_candidates, key=current_candidates.get)
        x, y = current
        neighbors = {
            p for p in {(x, min(y+1, ydim-1)), (x, max(y-1, 0)),
                        (min(x+1, xdim-1), y), (max(x-1, 0), y)}
            if p not in visited
        }
        for n in neighbors:
            distance = distances[current] + grid[n[1]][n[0]]
            if distance < distances[n]:
                distances[n] = distance
                paths[n] = paths[current] + [n]
        unvisited.remove(current)
        visited.add(current)
    return distances[dest], paths[dest]


def dijkstra2(start, end, graph):
    unvisited = set(graph.keys())
    visited = set()
    distances = {p: np.inf for p in univisited}
    distances[start] = 0
    # while unvisited:


# PART 1
@measure_time
def solve1(data):
    target = (len(data[0])-1, len(data)-1)
    distance, path = dijkstra((0, 0), target, data)
    return distance


# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

