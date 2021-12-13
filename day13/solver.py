import sys
import numpy as np

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    coordinates, _folds = raw_data.split("\n\n")
    points = []
    for c in coordinates.splitlines():
        x, y = c.split(",")
        points.append((int(x), int(y)))
    dimx = max(x for x, _ in points)
    dimy = max(y for _, y in points)
    paper = np.array([
        np.array([0 for _ in range(dimx + 1)])
        for _ in range(dimy + 1)
    ])
    for x, y in points:
        paper[y][x] = 1
    folds = []
    for f in _folds.splitlines():
        f = f.split()[2]
        axis, index = f.split("=")
        folds.append((axis, int(index)))
    return paper, folds


def foldup(paper, axis):
    upper = paper[:axis]
    lower = paper[(axis+1):][::-1]
    return upper + lower


def foldleft(paper, axis):
    right = paper[:, (axis+1):]
    left = paper[:, (axis-1)::-1]
    return right + left


# PART 1
@measure_time
def solve1(data):
    paper, folds = data
    axis, index = folds[0]
    if axis == "x":
        paper = foldleft(paper, index)
    else:
        paper = foldup(paper, index)
    return np.sum(paper>0)


# PART 2
@measure_time
def solve2(data):
    paper, folds = data
    for axis, index in folds:
        if axis == "x":
            paper = foldleft(paper, index)
        else:
            paper = foldup(paper, index)
    for line in paper:
        for point in line[::-1]:
            if point == 0:
                print(" ", end="")
            else:
                print("#", end="")
        print()


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

