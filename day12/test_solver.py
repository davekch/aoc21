import pytest
from solver import parse, solve1, solve2

TESTDATA = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

TESTDATA2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

TESTDATA3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

@pytest.fixture
def parsed_data():
    return [parse(d) for d in [
        TESTDATA, TESTDATA2, TESTDATA3
    ]]


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solutions = [10, 19, 226]
    for parsed, solution in zip(parsed_data, solutions):
        assert solve1(parsed) == solution


# PART 2
def test_solve2(parsed_data):
    solutions = [36, 103, 3509]
    for parsed, solution in zip(parsed_data, solutions):
        assert solve2(parsed) == solution
