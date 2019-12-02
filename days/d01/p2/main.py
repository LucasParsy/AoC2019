#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
import collections


class Event(NamedTuple):
    num: int
    ev: str


def main(lines: List[str]):
    res = 0
    for line in lines:
        fuel = int(line)
        while fuel > 0:
            fuel = int(fuel / 3) - 2
            res += fuel
        res -= fuel
    print(res)


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    #print_input(inputLines)
    main(inputLines)
