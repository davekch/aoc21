import pytest
from solver import parse, solve1, solve2

TESTDATA  = [
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
]


@pytest.fixture
def parsed_data():
    return [parse(test) for test in TESTDATA]


def test_parse():
    data = parse(TESTDATA[0])
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    testsolutions = [16, 12, 23, 31]
    for i, parsed in enumerate(parsed_data):
        solution = solve1(parsed)
        assert solution == testsolutions[i]


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
