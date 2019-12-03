#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
import collections


class Event(NamedTuple):
    ev: str
    num: int


class Point(NamedTuple):
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


GRIDSIZE = 50000


def path_machine(line: str) -> List[Point]:
    codes = [Event(x[0], int(x[1:])) for x in line.split(',')]
    x = y = 0
    path = []

    for elem in codes:
        if elem.ev == "R":
            for x in range(x, x + elem.num + 1):
                path.append(Point(x, y))
        elif elem.ev == "L":
            for x in range(x, x - elem.num - 1, -1):
                path.append(Point(x, y))
        elif elem.ev == "U":
            for y in range(y, y - elem.num - 1, -1):
                path.append(Point(x, y))
        elif elem.ev == "D":
            for y in range(y, y + elem.num + 1):
                path.append(Point(x, y))
    return path


def main(lines: List[str]):
    # grid = [[0] * GREIDSIZE] * GREIDSIZE
    l1 = path_machine(lines[0])
    l2 = path_machine(lines[1])
    # for line in grid:
    # print(line)

    start_pos = int(GRIDSIZE / 2)
    intersec = list(set(l1).intersection(l2))
    distances = []
    for elem in intersec:
        print(elem.y, elem.x)
        dist = abs(elem.x) + abs(elem.y)
        if dist != 0:
            distances.append(dist)
    print(min(distances))


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
