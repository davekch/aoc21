import sys

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    raw_data = raw_data.splitlines()
    data = [[] for _ in raw_data[0]]
    for line in raw_data:
        for i, bit in enumerate(line):
            data[i].append(bit)
    return data


# PART 1
@measure_time
def solve1(data):
    gamma = ""
    epsilon = ""
    for row in data:
        if row.count("1") > row.count("0"):
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    return int(gamma, base=2) * int(epsilon, base=2)


def sig_bit(i, data):
    data_T = list(map(list, zip(*data)))
    if data_T[i].count("1") >= data_T[i].count("0"):
        return "1"
    return "0"


# PART 2
@measure_time
def solve2(data):
    data = list(map(lambda l: "".join(l), zip(*data)))
    oxys = data[:]
    co2s = data[:]
    for i in range(len(data[0])):
        if len(oxys) == 1:
            break
        bit = sig_bit(i, oxys)
        oxys = list(filter(lambda b: b[i] == bit, oxys))
    for i in range(len(data[0])):
        if len(co2s) == 1:
            break
        bit = "1" if sig_bit(i, co2s) == "0" else "0"
        co2s = list(filter(lambda b: b[i] == bit, co2s))
    return int(oxys[0], base=2) * int(co2s[0], base=2)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

