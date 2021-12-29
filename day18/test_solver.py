import pytest
from solver import parse, solve1, solve2, SnailNumber, snailsum

TESTDATA = """[1,1]
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_snailexplode():
    examples = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ]
    for ex, solution in examples:
        sn = SnailNumber.fromstring(ex)
        assert str(sn) == ex
        sn.explode()
        assert str(sn) == solution


def test_manualreduce():
    sn1 = SnailNumber.fromstring("[[[[4,3],4],4],[7,[[8,4],9]]]")
    sn2 = SnailNumber.fromstring("[1,1]")
    sn = sn1 + sn2
    assert str(sn) == "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    assert sn.explode()
    assert str(sn) == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
    assert not sn.split()
    assert sn.explode()
    assert str(sn) == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    assert sn.split()
    assert str(sn) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    assert not sn.explode()
    assert sn.split()
    assert str(sn) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    assert sn.explode()
    assert str(sn) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert not sn.split()
    assert not sn.explode()



def test_reduce():
    sn1 = SnailNumber.fromstring("[[[[4,3],4],4],[7,[[8,4],9]]]")
    sn2 = SnailNumber.fromstring("[1,1]")
    sn = sn1 + sn2
    sn.reduce()
    assert str(sn) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"

def test_parse():
    data = parse(TESTDATA)
    # asserts go here


def test_snailsum():
    test1 = """[1,1]
[2,2]
[3,3]
[4,4]"""
    assert str(snailsum(parse(test1))) == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    test2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""
    assert str(snailsum(parse(test2))) == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
    test3 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
    assert str(snailsum(parse(test3))) == "[[[[5,0],[7,4]],[5,5]],[6,6]]"


def test_snailsum_detailed():
    test = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
    numbers = parse(test)
    ssum = numbers.pop(0)
    ssum = ssum + numbers.pop(0)
    ssum.reduce()
    assert str(ssum) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    ssum = ssum + numbers.pop(0)
    ssum.reduce()
    assert str(ssum) == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"




# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    # asserts go here


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
