import sys

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    displays = []
    for line in raw_data.splitlines():
        combinations, digits = line.split("|")
        combinations = [c.strip() for c in combinations.split()]
        digits = [d.strip() for d in digits.split()]
        displays.append((combinations, digits))
    return displays


# PART 1
@measure_time
def solve1(data):
    counter = 0
    for _, digits in data:
        for d in digits:
            if len(d) in [7,3,2,4]:
                counter += 1
    return counter


seven_segments = {
    "0": [1, 1, 1, 0, 1, 1, 1],
    "1": [0, 0, 1, 0, 0, 1, 0],
    "2": [1, 0, 1, 1, 1, 0, 1],
    "3": [1, 0, 1, 1, 0, 1, 1],
    "4": [0, 1, 1, 1, 0, 1, 0],
    "5": [1, 1, 0, 1, 0, 1, 1],
    "6": [1, 1, 0, 1, 1, 1, 1],
    "7": [1, 0, 1, 0, 0, 1, 0],
    "8": [1, 1, 1, 1, 1, 1, 1],
    "9": [1, 1, 1, 1, 0, 1, 1],
}

lengths = {k: v.count(1) for k, v in seven_segments.items()}


# PART 2
@measure_time
def solve2(data):
    numbers = []
    for combination, digits in data:
        possibilities_segments = [set("abcdefg") for _ in range(7)]
        possibilities_digits = {
            d: set(combination) for d in seven_segments
        }
        # handle obvious digits
        for c in combination:
            if len(c) == 2:
                digit = "1"
            elif len(c) == 3:
                digit = "7"
            elif len(c) == 4:
                digit = "4"
            elif len(c) == 7:
                digit = "8"
            else:
                digit = None
            if digit:
                possibilities_digits = {d: {c} if d==digit else p.difference({c}) for d,p in possibilities_digits.items()}
                for i, segment in enumerate(seven_segments[digit]):
                    if segment:
                        possibilities_segments[i] &= set(c)
                    else:
                        possibilities_segments[i] = possibilities_segments[i].difference(set(c))
        # print(combination)
        # print(possibilities_segments)
        # print(possibilities_digits)
        while any(len(p) > 1 for p in possibilities_digits.values()):
            # while there is any segment with an ambiguous code
            for d, ps in possibilities_digits.items():
                for p in ps:
                    letter_positions = {l: [i for i,seg in enumerate(possibilities_segments) if l in seg and seven_segments[d][i]] for l in p}
                    # print(f"{p=}, {letter_positions=}")
                    # if any two letters can only be at one position, this p is impossible
                    if any(list(letter_positions.values()).count(pos) > 1 and len(pos) == 1 for pos in letter_positions.values()):
                        # print(f"{p} can't be {d}!")
                        possibilities_digits[d] = possibilities_digits[d].difference({p})
            # remove any unique thingy from the other possibilities
            sure = [ps for ps in possibilities_digits.values() if len(ps) == 1]
            for d, ps in possibilities_digits.items():
                if ps in sure:
                    continue
                possibilities_digits[d] = possibilities_digits[d].difference({
                    s for s, in sure
                })
            # print(possibilities_digits)

        # inverse the possibilities dict
        codes = {next(iter(code)): digit for digit, code in possibilities_digits.items()}
        # print(codes)
        number = ""
        for d in digits:
            for c in codes:
                if set(c) == set(d):
                    number += codes[c]
        numbers.append(int(number))
    return sum(numbers)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

