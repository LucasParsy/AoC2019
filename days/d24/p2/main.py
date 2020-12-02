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
    center: int
    depthNegativeLevel = 1
    gameMap: Map2D
    centerNeighbors: Tuple(Tuple(int, int))
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def getpoint(self, x: int, y: int, gameMap: Map2D) -> bool:
        if (x < 0 or x >= self.boardSize or
                y < 0 or y >= self.boardSize):
            return False
        return gameMap[y][x]

    def generateEmptyMap(self) -> Map2D:
        return [[False] * self.boardSize for x in range(self.boardSize)]

    def __init__(self, mapStr: List[str]) -> None:
        self.boardSize = len(mapStr[0])
        center = (self.boardSize // 2)
        self.center = center
        self.centerNeighbors = [(center + x[0], center+x[1])
                                for x in self.directions]
        #print(self.centerNeighbors)

        self.gameMap = []
        for line in mapStr:
            lm = [c == '#' for c in line]
            self.gameMap.append(lm)

    def getHorizontalLinesBugs(self, grid: Map2D, index: int) -> int:
        return sum(grid[index])

    def getverticalLinesBugs(self, grid: Map2D, index: int) -> int:
        res = 0
        for line in grid:
            res += line[index]
        return res

    def getNumBugsAdj(self, depth: int, grids: List[Map2D], x: int, y: int) ->int:
        numAdj = 0
        for dir in self.directions:
            nx = x + dir[0]
            ny = y + dir[1]
            #print(depth, nx, ny)
            if depth != len(grids)-1:
                topGrid = grids[depth+1]
                if nx == -1:
                    numAdj += topGrid[self.center][self.center-1]
                if nx == self.boardSize:
                    numAdj += topGrid[self.center][self.center+1]
                if ny == -1:
                    numAdj += topGrid[self.center-1][self.center]
                if ny == self.boardSize:
                    numAdj += topGrid[self.center+1][self.center]
            if (nx == ny == self.center) and depth != 0:
                bottGrid = grids[depth-1]
                if x == self.center + 1: #right side
                    numAdj += self.getverticalLinesBugs(bottGrid, self.boardSize - 1)
                elif x == self.center - 1: #left
                    numAdj += self.getverticalLinesBugs(bottGrid, 0)
                elif y == self.center + 1: #bottom
                    numAdj += self.getHorizontalLinesBugs(bottGrid, self.boardSize - 1)
                elif y == self.center - 1: #top
                    numAdj += self.getHorizontalLinesBugs(bottGrid, 0)

            elif self.getpoint(nx, ny, grids[depth]):
                numAdj += 1
        return numAdj


    def step(self, gameMap: Map2D, depth: int,
             grids: List[Map2D], resMaps: List[Map2D]):
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if x == y == self.center:
                    continue
                hasBug = self.getpoint(x, y, gameMap)
                numAdj = self.getNumBugsAdj(depth, grids, x, y)
                if hasBug and numAdj != 1:
                    resMaps[depth][y][x] = False
                elif not hasBug and numAdj in (1, 2):
                    resMaps[depth][y][x] = True
                    if depth == len(grids)-1 and (x == 0 or x == self.boardSize-1 or
                                                  y == 0 or y == self.boardSize-1):
                        self.appendGrid = True
                    elif depth == 0 and (x, y) in self.centerNeighbors:
                        self.insertGrid = True


    def getNumBugs(self, grids: List[Map2D]):
        res = 0
        for g in grids:
            for line in g:
                res += sum(line)
        return res

    def showMap(self, gameMap: Map2D, depth: int):
        print(f"Depth {depth}:")
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if x == y == self.center:
                    print('?', end='')
                    continue
                print('#' if gameMap[y][x] else '.', end="")
            print()
        print()
        print()

    def solveP2(self) -> int:

        grids = [self.generateEmptyMap(),  self.gameMap,
                 self.generateEmptyMap()]
        for _ in range(200):
            self.insertGrid = False
            self.appendGrid = False

            nmaps = deepcopy(grids)

            for depth, g in enumerate(grids):
                self.step(g, depth, grids, nmaps)

            if self.insertGrid:
                nmaps.insert(0, self.generateEmptyMap())
                self.depthNegativeLevel += 1
            if self.appendGrid:
                nmaps.append(self.generateEmptyMap())
            grids = nmaps

        self.depthNegativeLevel = len(grids) - self.depthNegativeLevel - 1
        for depth, g in enumerate(reversed(grids)):
            self.showMap(g, depth - self.depthNegativeLevel)

        res = self.getNumBugs(grids)
        print("solution part 2:", res)
        return res


def main(lines: List[str]):
    p = GameOfLife(lines)
    p.solveP2()


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
