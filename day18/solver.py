import sys
from dataclasses import dataclass
from typing import Union, Optional
import json
from math import floor, ceil

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


@dataclass
class SnailNumber:
    left: Union[int, "SnailNumber"]
    right: Union[int, "SnailNumber"]

    def __add__(self, other: "SnailNumber") -> "SnailNumber":
        return SnailNumber(left=self, right=other)

    def __repr__(self) -> str:
        return f"[{self.left},{self.right}]"


    def __contains__(self, other: Union["SnailNumber", int]) -> bool:
        if self == other:
            return True
        if self.left == other:
            return True
        elif self.right == other:
            return True
        else:
            if isinstance(self.left, int) and self.left != other:
                lcontains = False
            else:
                lcontains = other in self.left
            if isinstance(self.right, int) and self.right != other:
                rcontains = False
            else:
                rcontains = other in self.right
            return lcontains or rcontains

    @classmethod
    def fromstring(cls, string: str) -> "SnailNumber":
        return cls.fromlist(json.loads(string))

    @classmethod
    def fromlist(cls, ls: list) -> "SnailNumber":
        a, b = ls
        if isinstance(a, list):
            a = cls.fromlist(a)
        if isinstance(b, list):
            b = cls.fromlist(b)
        return cls(left=a, right=b)

    def explode(self) -> bool:
        """explodes the snailfishnumber if the explode-rule applies and returns True,
        returns False if there was nothing to explode
        """
        print(f"exploding {self} --------------")
        # get a list of parents to a pair that is nested inside 4 layers
        parents = godeep(self, 4)
        if not parents:
            return False

        print(parents)
        snailnumber = parents.pop()
        assert isinstance(snailnumber.left, int) and isinstance(snailnumber.right, int)
        ldone = False
        rdone = False
        directparent = parents[-1]
        while parents:
            parent = parents.pop()
            print(f"looking at parent {parent}")
            if isinstance(parent.left, int) and not ldone:
                print(f"left is int ({parent.left}), add left snailnumber to it")
                parent.left += snailnumber.left
                ldone = True
            elif not ldone and snailnumber not in parent.left:
                print(f"left is a snailnumber! we must walk right")
                walkr(parent.left).right += snailnumber.left
                ldone = True
            if isinstance(parent.right, int) and not rdone:
                print(f"right is int ({parent.right}), add right snailnumber to it")
                parent.right += snailnumber.right
                rdone = True
            elif not rdone and snailnumber not in parent.right:
                print(f"right is a snailnumber! we must walk left")
                walkl(parent.right).left += snailnumber.right
                rdone = True
        # explode the original pair
        if directparent.left == snailnumber:
            directparent.left = 0
        else:
            directparent.right = 0
        return True

    def split(self) -> bool:
        """split the snailnumber if the split-rule applies and returns True,
        returns False if there is nothing to split
        """
        split = find_splitparent(self)
        if not split:
            return False
        if isinstance(split.left, int) and split.left >= 10:
            split.left = SnailNumber(left=floor(split.left/2), right=ceil(split.left/2))
        if isinstance(split.right, int) and split.right >= 10:
            split.right = SnailNumber(left=floor(split.right/2), right=ceil(split.right/2))
        return True

    def reduce(self):
        while self.explode() or self.split():
            continue


def godeep(snail: SnailNumber, n: int) -> Optional[list[SnailNumber]]:
    """
    traverse snail n layers deep, if the end-snailnumber is a pair of ints,
    return it together with a list of its parents
    """
    if n == 0:
        if isinstance(snail.left, int) and isinstance(snail.right, int):
            return [snail]
        else:
            return None
    if isinstance(snail.left, SnailNumber):
        leftparents = godeep(snail.left, n-1)
    else:
        leftparents = None
    if isinstance(snail.right, SnailNumber):
        rightparents = godeep(snail.right, n-1)
    else:
        rightparents = None
    if leftparents:
        return [snail] + leftparents
    if rightparents:
        return [snail] + rightparents
    return None


def find_splitparent(snail: SnailNumber) -> SnailNumber:
    if isinstance(snail.left, int):
        if snail.left >= 10:
            return snail
        else:
            lsplit = None
    else:
        lsplit = find_splitparent(snail.left)
    if isinstance(snail.right, int):
        if snail.right >= 10:
            return snail
        else:
            rsplit = None
    else:
        rsplit = find_splitparent(snail.right)
    return lsplit or rsplit


def walkl(snail: SnailNumber) -> SnailNumber:
    """traverse snail to the left until a single number is hit"""
    print(f"walkl {snail}")
    if isinstance(snail.left, int):
        return snail
    return walkl(snail.left)


def walkr(snail: SnailNumber) -> SnailNumber:
    """traverse snail to the right until a single number is hit"""
    print(f"walkr {snail}")
    if isinstance(snail.right, int):
        return snail
    return walkr(snail.right)


def snailsum(sns: list[SnailNumber]) -> SnailNumber:
    ssum, *rest = sns
    for sn in rest:
        ssum = ssum + sn
        ssum.reduce()
    return ssum


@measure_time
def parse(raw_data):
    return [SnailNumber.fromstring(sn) for sn in raw_data.splitlines()]


# PART 1
@measure_time
def solve1(data):
    pass


# PART 2
@measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

