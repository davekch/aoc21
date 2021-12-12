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


def step(octopi):
    flashcount = 0
    octopi += 1
    flash_coordinates = list(zip(*np.where(octopi>9)))
    # print(octopi)
    flashed = []
    while flash_coordinates:
        # print(f"{flash_coordinates=}")
        #if np.any(octopi>100):
        #    return -1
        for y, x in flash_coordinates:
            flashed.append((y, x))
            for j in range(max(y-1, 0), y+2):
                for i in range(max(x-1, 0), x+2):
                    try:
                        octopi[j][i] += 1
                    except IndexError:
                        continue
        flash_coordinates = list(c for c in zip(*np.where(octopi>9)) if c not in flashed)
        # print(octopi)
    octopi[octopi>9] = 0
    # print(octopi)
    return len(flashed)



# PART 1
@measure_time
def solve1(data):
    data = data.copy()
    count = 0
    for _ in range(100):
        c = step(data)
        # print(f"step {_} {c=}")
        if c == -1:
            break
        count += c
    return count


# PART 2
@measure_time
def solve2(data):
    i = 0
    while True:
        step(data)
        i += 1
        if np.all(data == 0):
            return i


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

