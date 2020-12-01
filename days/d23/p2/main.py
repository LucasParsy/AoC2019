#!/usr/bin/env python3

from __future__ import annotations
from itertools import combinations, permutations, count, islice

import sys
import pickle
from dataclasses import dataclass
from typing import Any, Callable, List, NamedTuple, Tuple, Dict, TypeVar
from copy import copy, deepcopy
from datetime import timedelta, datetime
from glob import glob
from intcode import Machine
import itertools
import math


def main(lines: List[str]):

    packets : List[Tuple(int, Tuple(int, int))] = []
    nat = []
    lastDeliveredNat = -126872589268515

    idleCount = 0
    idleCap = 1000

    machines = [Machine([i, -1], lines[0]) for i in range(50)]

    while all([not m.ended() for m in machines]):
        isIdle = True
        for m in machines:
            if m.ended():
                continue
            m.step()
            if len(m._output) == 3:
                isIdle = False
                dest = m._output[0]
                vals = m._output[1:]
                #print("dest:", dest)
                m._output = []
                if dest == 255:
                    if not nat:
                        print("solution part 1 is :", vals[1])
                    nat = vals
                    continue
                machines[dest]._input += vals
        if isIdle:
            idleCount += 1
        else:
            idleCount = 0
        if idleCount == idleCap:
            idleCount = 0
            machines[0]._input += nat
            if nat[1] == lastDeliveredNat:
                print("solution part 2 is :", lastDeliveredNat)
                return
            lastDeliveredNat = nat[1]

    print("ended machines")




def unique_test():
    pass

def fileTest(lines: List[str], expected: str):
    pass
    #assert(res == expected)


def unit_test():
    start = datetime.now()
    unique_test()
    for fname in glob("./tests/*.txt"):
        print("---",fname, "---")
        with open(fname, "r") as f:
            expected = fname.split('-')[1]
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            fileTest(inputLines, expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs")
    #if delta < bestTime:
        #print("new record!")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    # sys.setrecursionlimit(99999)
    unit_test()

    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
