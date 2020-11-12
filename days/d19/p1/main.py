#!/usr/bin/env python3

from __future__ import annotations
from itertools import combinations, permutations

import sys
import pickle
from dataclasses import dataclass
from typing import Any, List, NamedTuple, Tuple, Dict, TypeVar
from copy import copy, deepcopy
from datetime import timedelta, datetime
from glob import glob
from intcode import Machine
import itertools
import numpy as np

from Point import Point
import turtle_mode

@dataclass
class Tractor:

    def solveP1(self, lines: str):
        numPoints = 0
        res = []
        for x in range(50):
            for y in range(50):
                m = Machine([x, y], lines)
                mRes = m.run()
                mRes = mRes[0]
                numPoints += mRes
                c = '.' if mRes == 0 else "#"
                res.append(mRes)
                print(c, end="")
            print()
        print(numPoints)

    def getInitialPoints(self, y: int, lines: str) -> Tuple(List[int]):
        x = 0
        while(Machine([x, y], lines).run()[0] == 0):
            x += 1
        p1 = [x, y]
        while(Machine([x, y], lines).run()[0] == 1):
            x += 1
        p2 = [x-1,y]
        return (p1, p2)

    def getAngle(self, p1: List[int], p2: List[int]) -> int:
        unit_vector_1 = p1 / np.linalg.norm(p1)
        unit_vector_2 = p2 / np.linalg.norm(p2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        return np.arccos(dot_product)


    def getBestPoint(self, shipSize: int, p1: List[int], p2:List[int]) -> List[int]:
        angleTractor = self.getAngle(p1, p2)
        print("angle:", angleTractor, np.rad2deg(angleTractor))

        horizontal = [1000, 0]
        angleH = self.getAngle(p1, horizontal) + np.deg2rad(45)
        angleC = np.deg2rad(180) - angleH - angleTractor

        distP1 = np.linalg.norm(p1)
        distDiago = np.dot(distP1, np.sin(angleTractor)/np.sin(angleC))
        print()
        multip = np.sqrt(2* pow(shipSize, 2))/distDiago
        print(distDiago)
        print(p1, multip)
        resPoint = [int(p1[0] * multip)-1, int((p1[1] * multip) - shipSize)-1]
        print(resPoint)
        return resPoint

    def stupidSmartSolverThatDoesNotWork(self, lines: str):
        shipSize = 100
        y = 5000 # bigger = better angle precision, slower retreiving
        #p1, p2 = self.getInitialPoints(y, lines)
        p1 = [5095, 5000]
        p2 = [6331, 5000]
        #print(p1, p2)

        assert(self.getBestPoint(10, [19,22], [37, 22]) == [25, 20])
        resPoint = self.getBestPoint(shipSize, p1, p2)

        assert (Machine([resPoint[0], resPoint[1]], lines).run()[0] == 1)
        assert (Machine([resPoint[0]+ shipSize-1, resPoint[1]], lines).run()[0] == 1)
#        assert (Machine([resPoint[0]+ shipSize, resPoint[1]], lines).run()[0] == 0)
        assert (Machine([resPoint[0], resPoint[1] + shipSize-1], lines).run()[0] == 1)
        #assert (Machine([resPoint[0] - 1, resPoint[1] + shipSize-1], lines).run()[0] == 0)

        print(resPoint)
        resVal  = resPoint[0] * 10000 + resPoint[1]
        assert(resVal < 93608186)
        print(resVal)


    def solveP2(self, lines: str):
        shipSize = 100

        shipSize -= 1
        y = 150
        x = 0

        while True:
            while(Machine([x, y], lines).run()[0] == 0):
                x+=1
            if Machine([x+shipSize, y-shipSize], lines).run()[0] == 1:
                break
            y += 1

        y-= shipSize
        print(x, y)
        resVal  = x * 10000 + y
        print(resVal)


def main(lines: List[str]):
    t = Tractor()
    t.solveP1(lines[0])
    t.solveP2(lines[0])



def getPath(lines: List[str]):
    pass
    #maze = MazeGame(lines)
    #assert(maze.getPoint(maze.startPos) == '@')

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
            dist, _ = getPath(inputLines)
            assert(dist == expected)

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
    sys.setrecursionlimit(1500)
    #unit_test()
    
    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
