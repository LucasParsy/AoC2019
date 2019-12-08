#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections


class Event(NamedTuple):
    num: int
    ev: str


def main(lines: List[str]):
    width = 25
    height = 6
    image_size = width * height
    line_num = [int(x) for x in list(lines[0])]
    layers = [line_num[x:x + image_size] for x in range(0, len(line_num), image_size)]
    num_zero = [lay.count(0) for lay in layers]
    print(num_zero)
    lay_index = num_zero.index(min(num_zero))
    res = layers[lay_index].count(1) * layers[lay_index].count(2)
    print(res)


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
