import sys
import numpy as np

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [int(x) for x in raw_data.split(",")]


# PART 1
@measure_time
def solve1(data):
    mn = min(data)
    mx = max(data)
    data = np.array(data)
    fuels = [abs(data - pos).sum() for pos in range(mn, mx+1)]
    return min(fuels)


# PART 2
@measure_time
def solve2(data):
    mn = min(data)
    mx = max(data)
    fuels = []
    fuel_lookup = {}
    for pos in range(mn, mx+1):
        i_fuels = []
        for x in data:
            if x-pos not in fuel_lookup:
                fuel_lookup[x-pos] = sum(range(abs(x-pos) + 1))
            i_fuels.append(fuel_lookup[x-pos])
        fuels.append(sum(i_fuels))
    return min(fuels)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

