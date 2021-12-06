from functools import wraps
from datetime import datetime
import sys

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [int(n) for n in raw_data.splitlines()]


# PART 1
@measure_time
def solve1(data):
    diffs = [n2 - n1 for n1, n2 in zip(data, data[1:])]
    return len(list(filter(lambda n: n>0, diffs)))


# PART 2
@measure_time
def solve2(data):
    windows = []
    for i, n in enumerate(data):
        try:
            windows.append(n + data[i+1] + data[i+2])
        except IndexError:
            break
    windowdiffs = [w2 - w1 for w1, w2 in zip(windows, windows[1:])]
    return len(list(filter(lambda n: n>0, windowdiffs)))


if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))
