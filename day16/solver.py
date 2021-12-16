import sys
from io import StringIO

sys.path.insert(0, "../utils/py")
import utils


measure_time = utils.stopwatch()


def read_literal(stream: StringIO) -> int:
    leading = stream.read(1)
    numbers = [stream.read(4)]
    while leading == "1":
        leading = stream.read(1)
        numbers.append(stream.read(4))
    return int("".join(numbers), base=2)


def read_package(stream: StringIO) -> dict:
    version = stream.read(3)
    if not version:
        return None
    version = int(version, base=2)
    typeID = int(stream.read(3), base=2)
    packet = {
        "version": version,
        "typeID": typeID,
    }
    if typeID == 4:
        value = read_literal(stream)
        packet["value"] = value
    else:
        lengthtypeID = int(stream.read(1))
        packet["lengthtypeID"] = lengthtypeID
        packet["subpackets"] = []
        if lengthtypeID == 0:
            length = int(stream.read(15), base=2)
            substream = StringIO(stream.read(length))
            while (subpacket := read_package(substream)):
                packet["subpackets"].append(subpacket)
        elif lengthtypeID == 1:
            n_packets = int(stream.read(11), base=2)
            for _ in range(n_packets):
                packet["subpackets"].append(read_package(stream))
    return packet


@measure_time
def parse(raw_data):
    translate = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    bitstring = ""
    for c in raw_data:
        bitstring += translate[c]
    return bitstring


def sum_versions(package):
    if "subpackets" not in package:
        return package["version"]
    return package["version"] + sum(sum_versions(p) for p in package["subpackets"])


# PART 1
@measure_time
def solve1(data):
    stream = StringIO(data)
    packet = read_package(stream)
    return sum_versions(packet)


def calc_expr(packet: dict) -> int:
    match packet["typeID"]:
        case 4:
            return packet["value"]
        case 0:
            return sum(calc_expr(p) for p in packet["subpackets"])
        case 1:
            product = calc_expr(packet["subpackets"][0])
            for p in packet["subpackets"][1:]:
                product *= calc_expr(p)
            return product
        case 2:
            return min(calc_expr(p) for p in packet["subpackets"])
        case 3:
            return max(calc_expr(p) for p in packet["subpackets"])
        case 5:
            first, second = packet["subpackets"]
            return int(calc_expr(first) > calc_expr(second))
        case 6:
            first, second = packet["subpackets"]
            return int(calc_expr(first) < calc_expr(second))
        case 7:
            first, second = packet["subpackets"]
            return int(calc_expr(first) == calc_expr(second))


# PART 2
@measure_time
def solve2(data):
    stream = StringIO(data)
    packet = read_package(stream)
    return calc_expr(packet)


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print("Part 1: {}".format(solve1(data)))
    print("Part 2: {}".format(solve2(data)))

    print("\nTime taken:")
    for func, time in measure_time.times:
        print(f"{func:8}{time}s")
    print("----------------")
    print("total   {}s".format(sum(t for _, t in measure_time.times)))

