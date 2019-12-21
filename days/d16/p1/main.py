#!/usr/bin/env python3

from __future__ import annotations

import sys
import copy
import time
import curses
from dataclasses import dataclass
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple, TextIO
from inspect import signature
import collections
import turtle


@dataclass
class Operation:
    signal: List[int]

    num_phases: int = 100

    def calculate(self):
        sig_len = len(self.signal) + 1
        for phase in range(0, self.num_phases):
            ns = []
            for repeat in range(1, sig_len):
                digit = 0
                for ind in range(repeat - 1, sig_len, repeat * 4):
                    digit += sum(self.signal[ind:ind + repeat])
                    digit -= sum(self.signal[ind + repeat * 2:ind + repeat * 3])
                ns.append(abs(digit) % 10)
            self.signal = ns


def main(lines: List[str]):
    l = [int(x) for x in list(lines[0])]
    op = Operation(l)
    op.calculate()
    print(*op.signal[:8], sep="")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
