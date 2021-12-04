import sys
import itertools
from operator import itemgetter
from sortedcontainers import SortedList

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@measure_time
def parse(raw_data):
    raw_data = raw_data.splitlines()
    draw = [int(n) for n in raw_data[0].split(",")]
    boards = []
    board = []   # the current board
    for line in raw_data[2:]:
        if not line:
            boards.append(board)
            board = []
        else:
            board.append([int(n) for n in line.split()])
    boards.append(board)
    return (draw, boards)


def find_marked(draw, board):
    for j, row in enumerate(board):
        try:
            i = row.index(draw)
            return (j, i)
        except ValueError:
            continue


def find_winner(marked):
    for k, board in marked.items():
        # print(f"board {k}")
        rows = itertools.groupby(sorted(board, key=itemgetter(0)), key=itemgetter(0))
        # print("rows")
        for j, group in rows:
            # print(list(group))
            if len(list(group)) == 5:
                return k
        columns = itertools.groupby(sorted(board, key=itemgetter(1)), key=itemgetter(1))
        # print("columns")
        for i, group in columns:
            # print(list(group))
            if len(list(group)) == 5:
                return k


# PART 1
@measure_time
def solve1(data):
    draws, boards = data
    marked = {k: [] for k in range(len(boards))}
    for draw in draws:
        # print()
        # print(f"draw {draw}")
        for k, board in enumerate(boards):
            coordinates = find_marked(draw, board)
            if coordinates:
                marked[k].append(coordinates)
        # print(marked)
        winner = find_winner(marked)
        if winner is not None:
            # print(f"board {k} wins with {draw}")
            score = sum(boards[winner][j][i] for j in range(5) for i in range(5) if (j, i) not in marked[winner])
            # print(score)
            return draw * score


# PART 2
@measure_time
def solve2(data):
    draws, boards = data
    marked = {k: [] for k in range(len(boards))}
    won = []
    for draw in draws:
        for k, board in enumerate(boards):
            # print(f"checking board {k}, won: {won}")
            if k not in won:
                coordinates = find_marked(draw, board)
                if coordinates:
                    marked[k].append(coordinates)
                winner = find_winner(marked)
                if winner is not None:
                    # print(f"board {winner} wins with {draw}")
                    if len(won) == len(boards) - 1:
                        score = sum(boards[winner][j][i] for j in range(5) for i in range(5) if (j, i) not in marked[winner])
                        return score * draw
                    else:
                        won.append(winner)
                        # print(f"kicking out {winner}")
                        marked.pop(winner)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

