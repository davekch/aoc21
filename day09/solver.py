import sys
import numpy as np

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return np.array([
        np.array(list(map(int, line)))
        for line in raw_data.splitlines()
    ])


def get_lowpoint_mask(data):
    shifted_up = np.vstack([data[1:, :], np.full([1, data.shape[1]], np.inf)])
    shifted_down = np.vstack([np.full([1, data.shape[1]], np.inf), data[:-1, :]])
    shifted_left = np.hstack([data[:, 1:], np.full([data.shape[0], 1], np.inf)])
    shifted_right = np.hstack([np.full([data.shape[0], 1], np.inf), data[:, :-1]])
    diff_up = data - shifted_down < 0
    diff_down = data - shifted_up < 0
    diff_left = data - shifted_right < 0
    diff_right = data - shifted_left < 0
    return diff_up & diff_down & diff_left & diff_right


# PART 1
@measure_time
def solve1(data):
    mask = get_lowpoint_mask(data)
    return sum(data[mask] + 1)


def walk(data, point, seen):
    if point in seen:
        return seen
    seen.add(point)
    xmax = len(data[0])
    ymax = len(data)
    # print(f"{point=}")
    y0, x0 = point
    news = set()
    if x0 + 1 < xmax and data[y0][x0+1] < 9:
        news.add((y0, x0+1))
    if x0 - 1 >= 0 and data[y0][x0-1] < 9:
        news.add((y0, x0-1))
    if y0 + 1 < ymax and data[y0+1][x0] < 9:
        news.add((y0+1, x0))
    if y0 - 1 >= 0 and data[y0-1][x0] < 9:
        news.add((y0-1, x0))
    for p in news:
        seen.update(walk(data, p, seen))
    return seen


# PART 2
@measure_time
def solve2(data):
    # print(data)
    xmax = len(data[0])
    ymax = len(data)
    # print(f"{xmax=}, {ymax=}")
    mask = get_lowpoint_mask(data)
    lowpoint_coordinates = zip(*np.where(mask==True))
    basins = []
    for p in lowpoint_coordinates:
        basin = walk(data, p, set())
        basins.append(len(basin))
    basins.sort(reverse=True)
    return basins[0] * basins[1] * basins[2]


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

