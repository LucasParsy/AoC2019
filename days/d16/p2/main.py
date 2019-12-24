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
            s = 0
            for repeat in range(sig_len - 2, -1, -1):
                s += self.signal[repeat]
                ns.append(s % 10)
                # print(*ns, sep="")
            ns.reverse()
            self.signal = ns
            #print(*self.signal, sep="")


def main(lines: List[str]):
    offset = int(lines[0][:7])
    l = [int(x) for x in list(lines[0])]
    l *= 10000
    l = l[offset:]
    op = Operation(l)
    op.calculate()
    print(*op.signal[0:8], sep="")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
