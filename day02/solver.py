from functools import wraps
from datetime import datetime


times = []


def measure_time(func):
    @wraps(func)
    def _func(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        times.append((func.__name__, (end - start).total_seconds()))
        return result

    return _func


@measure_time
def parse(raw_data):
    data = []
    for line in raw_data.splitlines():
        direction, x = line.split()
        data.append((direction, int(x)))
    return data


def move(pos, instructions):
    x, d = pos
    for instruction in instructions:
        match instruction:
            case ("forward", dx):
                x += dx
            case ("down", dd):
                d += dd
            case ("up", dd):
                d -= dd
    return (x, d)


def move_aim(apos, instructions):
    aim, x, d = apos
    for instruction in instructions:
        match instruction:
            case ("forward", dx):
                x += dx
                d += aim * dx
            case ("down", da):
                aim += da
            case ("up", da):
                aim -= da
    return (aim, x, d)


# PART 1
@measure_time
def solve1(data):
    x, d = move((0, 0), data)
    return x * d


# PART 2
@measure_time
def solve2(data):
    _, x, d = move_aim((0, 0, 0), data)
    return x * d


if __name__ == "__main__":
    import sys

    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in times)))
