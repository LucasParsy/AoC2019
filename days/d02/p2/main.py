#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
import collections


class Event(NamedTuple):
    num: int
    ev: str


def machine(lines, noun, verb):
    codes = [int(x) for x in lines[0].split(',')]
    codes[1] = noun
    codes[2] = verb

    for i in range(0, len(codes), 4):
        op = codes[i]
        a1 = codes[i + 1]
        a2 = codes[i + 2]
        a3 = codes[i + 3]

        if op == 1:
            codes[a3] = codes[a1] + codes[a2]
        if op == 2:
            codes[a3] = codes[a1] * codes[a2]
        if op == 99:
            break

    return codes[0]


def main(lines: List[str]):
    expected_out = 19690720

    for noun in range(0, 100):
        for verb in range(0, 100):
            if machine(lines, noun, verb) == expected_out:
                print(100 * noun + verb)
                exit()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
