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


def check_condition(s: str) -> bool:
    prev = '0'
    for c in s:
        if c < prev:
            return False
        prev = c

    num_list = list(s)
    for i in range(0, 10):
        if num_list.count(str(i)) == 2:
            return True
    return False


def main(lines: List[str]):
    interval = lines[0].split('-')
    sol = 0
    for i in range(int(interval[0]), int(interval[1])):
        s = str(i)
        if check_condition(s):
            sol += 1
    print("solution:", sol)


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
