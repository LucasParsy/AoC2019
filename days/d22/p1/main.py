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

from Point import Point
from intcode import Machine


class CardDealer:

    def cut(self, cards: List[int], index: int) -> List[int]:
        l1 = cards[index:]
        l2 = cards[:index]
        return l1 + l2

    def dealIncrement(self, cards: List[int], increment: int) -> List[int]:
        cardsLen = len(cards)
        nl = [-1] * cardsLen
        incInd = 0
        for i in range(cardsLen):
            nl[incInd% cardsLen] = cards[i]
            incInd += increment
        return nl

    def dealStack(self, cards: List[int]):
        cards.reverse()

    def solveP1(self, lines: List[str], numCards: int) -> List[int]:
        cards = list(range(0, numCards))
        for instruction in lines:
            words = instruction.split(" ")
            if words[0] == "cut":
                cards = self.cut(cards, int(words[-1]))
            elif words[1] == "with":
                cards = self.dealIncrement(cards, int(words[-1]))
            else:
                self.dealStack(cards)
        return cards


def main(lines: List[str]):
    dealer = CardDealer()
    res = dealer.solveP1(lines, 10007)
    #res = maze.solveP2(lines)
    print(res.index(2019))


def getPath(lines: List[str]) -> str:
    dealer = CardDealer()
    res = dealer.solveP1(lines, 10)
    res = [str(i) for i in res]
    return "".join(res)


def unit_test():
    gettrace = getattr(sys, 'gettrace', None)
    bestTime = 0.099888
    if gettrace and gettrace():
        bestTime = 0.472323

    start = datetime.now()

    for fname in glob("./tests/*.txt"):
        with open(fname, "r") as f:
            expected = fname.split('-')[1]
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            res = getPath(inputLines)
            assert(res == expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs. best:", bestTime)
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
