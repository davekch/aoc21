import sys
from enum import Enum
from bidict import bidict
from typing import Optional
from queue import LifoQueue

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


Result = Enum("Result", (
    "Ok",
    "Incomplete",
    "Corrupted"
))


brackets = bidict({
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
})

error_score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

incomplete_score = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

def check_syntax(line: str) -> tuple[Result, Optional[str | list]]:
    # print(line)
    queue = LifoQueue()
    for char in line:
        if char in brackets:
            # print(f"pushing {char} on queue")
            queue.put(char)
        elif char in brackets.inverse:
            if queue.empty():
                return (Result.Corrupted, char)
            opening = queue.get()
            # print(f"pop {opening} from queue, checking with {char}")
            if char != brackets[opening]:
                # print(f"syntax error! {char} is not {brackets[opening]}")
                return (Result.Corrupted, char)
        else:
            raise ValueError(f"unexpected character found: {char}")
    if queue.empty():
        return (Result.Ok, None)
    else:
        return (Result.Incomplete, [brackets[m] for m in reversed(queue.queue)])


@measure_time
def parse(raw_data):
    return [check_syntax(line) for line in raw_data.splitlines()]


# PART 1
@measure_time
def solve1(data):
    score = 0
    for result, error in data:
        if result == Result.Corrupted:
            score += error_score[error]
    return score


# PART 2
@measure_time
def solve2(data):
    scores = []
    for result, missing in data:
        score = 0
        if result == Result.Incomplete:
            for m in missing:
                score *= 5
                score += incomplete_score[m]
            scores.append(score)
    return sorted(scores)[len(scores)//2]


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

