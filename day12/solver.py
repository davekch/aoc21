import sys
from collections import defaultdict

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    graph = defaultdict(list)
    for line in raw_data.splitlines():
        node1, node2 = line.split("-")
        if node2 != "start":
            graph[node1].append(node2)
        if node1 != "start":
            graph[node2].append(node1)
    return graph


def walk(graph, start, seen):
    stops = graph[start]
    count = 0
    for stop in stops:
        if stop.islower() and stop in seen:
            continue
        if stop == "end":
            count += 1
            # print(",".join(seen) + f",{start}")
            continue
        count += walk(graph, stop, seen + [start])
    return count


def walktwice(graph, start, seen):
    stops = graph[start]
    count = 0
    for stop in stops:
        # print(f"we have a situation here: checking {stop}, leaving {','.join(seen)} behind me coming from {start}")
        # print("any lowercase stops have already been seen twice: ", any(seen.count(s) > 1 for s in seen if s.islower()))
        # print(f"{stop=}, {seen=}")
        if stop == "end":
            count += 1
            # print(",".join(seen) + f",{start}")
            continue
        if stop.islower():
            if stop in seen and any((seen + [start]).count(s) > 1 for s in seen if s.islower()):
                # print(f"jumping over {stop} because rules")
                continue
        # print(f"doing it because stupid; {stop=}, {seen=}")
        count += walktwice(graph, stop, seen + [start])
    return count


# PART 1
@measure_time
def solve1(data):
    return walk(data, "start", [])


# PART 2
@measure_time
def solve2(data):
    return walktwice(data, "start", [])


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

