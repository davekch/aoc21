import sys
from dataclasses import dataclass
from collections import Counter

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@dataclass
class LinkedList:
    value: str
    right: "LinkedList" = None

    @classmethod
    def fromlist(cls, ls):
        last = cls(value=ls.pop())
        for _ in range(len(ls)):
            v = ls.pop()
            last = cls(value=v, right=last)
        return last


@measure_time
def parse(raw_data):
    lines = raw_data.splitlines()
    polymer = list(lines[0])
    rules = {}
    for rule in lines[2:]:
        pair, ins = rule.split(" -> ")
        rules[pair] = ins
    return polymer, rules


# PART 1
@measure_time
def solve1(data):
    polymer, rules = data
    for _ in range(10):
        new = []
        for a,b in zip(polymer, polymer[1:]):
            new.append(a)
            new.append(rules[a+b])
        new.append(b)
        polymer = new
    counter = Counter(polymer)
    return max(counter.values()) - min(counter.values())


# PART 2
@measure_time
def solve2(data):
    polymer, rules = data
    # print(rules)
    paircounter = Counter([a+b for a, b in zip(polymer, polymer[1:])])
    # print(polymer)
    # print(paircounter)
    for _ in range(40):
        newcounter = Counter()
        for pair, c in paircounter.items():
            insert = rules[pair]
            newcounter[pair[0] + insert] += c
            newcounter[insert + pair[1]] += c
        paircounter = newcounter
    counter = Counter()
    for pair, count in paircounter.items():
        # counter[pair[0]] += count
        # this assumes that the first character is neither the max nor the min one
        counter[pair[1]] += count
    return max(counter.values()) - min(counter.values())


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

