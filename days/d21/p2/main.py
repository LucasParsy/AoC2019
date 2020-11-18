#!/usr/bin/env python3

from __future__ import annotations
from itertools import combinations, permutations

import sys
import pickle
from dataclasses import dataclass
from typing import Any, Callable, List, NamedTuple, Tuple, Dict, TypeVar
from copy import copy, deepcopy
from datetime import timedelta, datetime
from glob import glob
import itertools

from intcode import Machine


class MazeGame:
    machine: Machine

    def listStrintToIntInput(self, inp: List[str]) -> List[int]:
        s = "\n".join(inp) + "\n"
        return [ord(c) for c in s]

    def printIntOutput(self, out: List[int]):
        s = [chr(c) for c in out]
        print("".join(s))

    def tryInput(self, lines: List[str], inp: List[str]) -> int:
        inp = self.listStrintToIntInput(inp)
        m = Machine(inp, lines[0])
        res = m.run()
        if len(res) == 14:
            return res[13]
        else:
            self.printIntOutput(res)
            return -1

    def solveP1(self, lines: List[str]) -> int:
        inp = ["NOT A J",
               "NOT C T",
               "AND D T",
               "OR  T J",
               "WALK"]
        return self.tryInput(lines, inp)

    def solveP2(self, lines: List[str]) -> int:
        # rule 0:  Jump if A .                     (do not fall in pits)
        # rule 1:  Jump if C . and D #             (####.##..#.#####)
        # rule 1s: do not jump if not E and not H  (this single case: ####.#.##.####)
        # rule 2: Jump if B . and A and D          ( #####.##.##...###)

        inp = [             # _
            "OR E T",       #  | 1s
            "OR H T",       # _|
            "AND D T",      #  |
            "NOT C J",      #  | 1
            "AND T J",      # _|
            "NOT B T",      #  |
            "AND A T",      #  | 2
            "AND D T",      #  |
            "OR T J",       # _|
            "NOT A T",      #  |
            "OR  T J",      #  | 0
            "RUN"]          # _|

        return self.tryInput(lines, inp)


def main(lines: List[str]):
    maze = MazeGame()
    assert(maze.solveP1(lines) == 19349530)
    res = maze.solveP2(lines)
    print(res)


def getPath(lines: List[str]) -> int:
    maze = MazeGame()
    return maze.solveP1(lines)


def unit_test():
    gettrace = getattr(sys, 'gettrace', None)
    bestTime = 0.099888
    if gettrace and gettrace():
        bestTime = 0.472323

    start = datetime.now()

    for fname in glob("./tests/*.txt"):
        with open(fname, "r") as f:
            expected = int(fname.split('-')[1])
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            res = getPath(inputLines)
            assert(res == expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs. best:", bestTime)
    if delta < bestTime:
        print("new record!")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    # sys.setrecursionlimit(99999)
    # unit_test()

    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
