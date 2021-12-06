import sys
from collections import Counter

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    return [int(x) for x in raw_data.split(",")]


def life(counter, days):
    for _ in range(days):
        # print(f"day {_}: {counter}")
        if counter[0]:
            counter[7] += counter[0]
            counter[9] += counter[0]
            counter[0] = 0

        counter = Counter({
            k-1: v for k, v in counter.items() if k != 0
        })
    return counter


# PART 1
@measure_time
def solve1(data):
    counter = Counter(data)
    counter = life(counter, 80)
    return sum(counter.values())


# PART 2
@measure_time
def solve2(data):
    counter = Counter(data)
    counter = life(counter, 256)
    return sum(counter.values())


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

