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
import itertools
import math

Map2D = List[List[bool]]


@dataclass
class GameOfLife:
    boardSize: int
    gameMap: Map2D
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def getpoint(self, x: int, y: int, gameMap: Map2D) -> bool:
        if (x < 0 or x >= self.boardSize or
                y < 0 or y >= self.boardSize):
            return False
        return gameMap[y][x]

    def __init__(self, mapStr: List[str]) -> None:
        self.boardSize = len(mapStr[0])
        self.gameMap = []
        for line in mapStr:
            lm = [c == '#' for c in line]
            self.gameMap.append(lm)

    def step(self, gameMap: Map2D) -> Map2D:
        res = deepcopy(gameMap)
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                numAdj = 0
                hasBug = self.getpoint(x, y, gameMap)
                for dir in self.directions:
                    if self.getpoint(x+dir[0], y+dir[1], gameMap):
                        numAdj += 1
                if hasBug and numAdj != 1:
                    res[y][x] = False
                elif not hasBug and numAdj in (1, 2):
                    res[y][x] = True
        return res

    def getBiodivRating(self, gameMap: Map2D) -> int :
        res = 0
        numPow = 0
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if gameMap[y][x]:
                    res += pow(2, numPow)
                numPow += 1
        return res

    def showMap(self, gameMap: Map2D):
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                print('#' if gameMap[y][x] else '.', end="")
            print()
        print()
        print()

    def solveP1(self) -> int:
        ratings = []
        gmap = self.gameMap
        while True:
            #self.showMap(gmap)
            note = self.getBiodivRating(gmap)
            if note in ratings:
                print("solution step 1:", note)
                return note
            ratings.append(note)
            gmap = self.step(gmap)



def main(lines: List[str]):
    p = GameOfLife(lines)
    p.solveP1()


def unique_test():
    pass


def fileTest(lines: List[str], expected: str):
    pass
    #assert(res == expected)


def unit_test():
    start = datetime.now()
    unique_test()
    for fname in glob("./tests/*.txt"):
        print("---", fname, "---")
        with open(fname, "r") as f:
            expected = fname.split('-')[1]
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            fileTest(inputLines, expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs")
    # if delta < bestTime:
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
