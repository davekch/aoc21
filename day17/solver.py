import sys
import re
import math

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    numbers = re.findall("[-]?[0-9]+", raw_data)
    return ((int(numbers[0]), int(numbers[1])), (int(numbers[2]), int(numbers[3])))


def in_target(point, target):
    (xmin, xmax), (ymin, ymax) = target
    x, y = point
    return (xmin <= x <= xmax) and (ymin <= y <= ymax)


# PART 1
@measure_time
def solve1(data):
    # x velocity is irrelevant for this problem
    # the y position always comes back to 0 and has a velocity of vy_0 + 1
    # from here it must not pass beyond the target
    # the max height is sum(range(vy)+1)
    _, (ymin, ymax) = data
    max_vy = abs(min(ymin, ymax)) - 1
    return sum(range(max_vy+1))


# PART 2
@measure_time
def solve2(data):
    (xmin, xmax), (ymin, ymax) = data
    max_vy = abs(min(ymin, ymax)) - 1
    min_vy = min(ymin, ymax)  # the lower border of the target
    max_vx = xmax
    min_vx = math.ceil(max(
        (-1 + math.sqrt(1 + 8*xmin)) / 2,
        (-1 - math.sqrt(1 + 8*xmin)) / 2
    ))
    n = 0
    for _vx in range(min_vx, max_vx+1):
        for vy in range(min_vy, max_vy+1):
            v = (_vx, vy)
            vx = _vx
            hits = []
            x, y = 0, 0
            while x <= xmax and y >= ymin:
                x += vx
                vx = vx - 1 if vx > 0 else 0
                y += vy
                vy -= 1
                hits.append((x, y))
            if any(in_target(p, data) for p in hits):
                n += 1
    return n


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

