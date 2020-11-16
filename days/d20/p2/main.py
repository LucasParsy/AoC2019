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


@dataclass
class Path:
    distance: int
    path: List[Point]
    doors: List[str]


# typings
T = TypeVar('T', int,  List[Point],  List[str])
Combinations = Dict[str, Dict[str, Path]]


class MazeGame:
    gsx: int
    gsy: int

    numLevels: int = 30
    map: List[str]
    dijkstra_maps = List[List[int]]

    directions: List[Point]

    backtrack: List[int]
    badPath: Path
    wallsChar: List[str]
    atInd: int
    startPos: Point
    endPos: Point
    teleporters: Dict(Point, List[Any])

    def getPoint(self, p: Point) -> str:
        # on enlève la condition car On vit dans le Danger. pis y'a des murs partout
        # if p.x < 0 or p.y < 0 or p.x >= self.gsx or p.y >= self.gsy:
        #    return '#'
        return self.map[p.y * self.gsx + p.x]

    def getPointFromIndex(self, index: int) -> Point:
        return Point(index % self.gsx, int(index / self.gsx))

    def get_map_pos(self, map: List[int], pos: Point) -> int:
        return map[pos.y * self.gsx + pos.x]

    def __init__(self, lines: List[str], isSpecialCase=False):
        self.gsx = len(lines[0])
        self.gsy = len(lines)
        self.map = "".join(lines)
        self.getTeleporters(lines)

        dijkstra_map = [-2 if x != '.' else 99999 for x in self.map]
        self.dijkstra_maps = [copy(dijkstra_map)
                              for _ in range(0, self.numLevels)]

        self.directions = [Point(-1, 0), Point(0, -1),
                           Point(1, 0), Point(0, 1)]

        self.badPath = Path(9999, [], [])

    def putTeleportersPoint(self, st: str, pos: Point, levelInc: int):
        if st == "AA":
            self.startPos = pos
        elif st == "ZZ":
            self.endPos = pos
        else:
            data = [st]
            inverted = [x for x in self.teleporters.items() if
                        x[1][0] == st]
            if inverted:
                inverted = inverted[0]
                data.append(inverted[0])
                inverted[1].insert(1, pos)
            data.append(levelInc)
            self.teleporters[pos] = data

    def readVertical(self, lines: List[str], lineNum: int,
                     isTeleporterAbove: bool, levelInc: int, enumStart: int = 2, enumEnd: int = -2):
        for x, c in enumerate(lines[lineNum][enumStart: enumEnd]):
            if c != ' ':
                c2 = lines[lineNum+1][x+enumStart]
                if c2 == ' ':
                    continue
                pointY = +2 if isTeleporterAbove else -1
                self.putTeleportersPoint(c + c2,
                                         Point(x + enumStart, lineNum + pointY), levelInc)

    def readHorizontal(self, lines: List[str], charNum: int,
                       isTeleporterLeft: bool, levelInc: int, enumStart: int = 2, enumEnd: int = -2):
        for y, l in enumerate(lines[enumStart:enumEnd]):
            if l[charNum] != ' ':
                c2 = l[charNum+1]
                if c2 == ' ':
                    continue
                pointX = +2 if isTeleporterLeft else -1
                self.putTeleportersPoint(l[charNum] + c2,
                                         Point(charNum+pointX, y+enumStart), levelInc)

    def genericReadDirection(self, lines: List[str], method: Callable,
                             axes: Tuple(int), tCenter: int):
        enumEnd = axes[1]-tCenter
        method(lines, 0, True, -1)
        method(lines, axes[0]-2, False, -1)
        method(lines, tCenter, False, 1, tCenter, enumEnd)
        method(lines, axes[0]-2-tCenter, True, 1, tCenter, enumEnd)

    def getTeleporters(self, lines: List[str]):
        self.teleporters = {}
        tCenter = 0
        for x, c in enumerate(lines[self.gsy // 2][2:]):
            if c not in ['.', '#']:
                tCenter = x + 2
                break
        #print("torusCenter:", tCenter)
        self.genericReadDirection(
            lines, self.readHorizontal, (self.gsx, self.gsy), tCenter)
        self.genericReadDirection(
            lines, self.readVertical, (self.gsy, self.gsx), tCenter)
        #print(self.teleporters)

    def print_dijkstra_map(self):
        for y in range(0, self.gsy):
            for x in range(y*(self.gsx), (y+1)*(self.gsx)):
                print("{:^4}".format(self.dijkstra_maps[0][x]), end="")
            print()

    def dijkstra_recursive_mapping(self, maps: List[List[int]], currPoint: Point,
                                   distance: int, level: int, hasTeleported=False):
        if distance == 9999:
            return
        pos = currPoint.y * self.gsx + currPoint.x
        if maps[level][pos] <= distance or maps[level][pos] == -2:
            return
        maps[level][pos] = distance
        tel = self.teleporters.get(currPoint)
        if not hasTeleported and tel:
            nextPoint = tel[1]
            newLevel = level + tel[2]
            if newLevel >= 0 and newLevel < self.numLevels:
                self.dijkstra_recursive_mapping(
                    maps, nextPoint, distance+1, newLevel, True)
            return

        for dir in self.directions:
            nextPoint = currPoint + dir
            self.dijkstra_recursive_mapping(maps, nextPoint, distance+1, level)

    def dijkstra_path_key(self, startPos: Point, searchedPos: Point) -> Path:
        self.dijkstra_recursive_mapping(self.dijkstra_maps, startPos, 0, 0)
        maxDist = self.get_map_pos(self.dijkstra_maps[0], searchedPos)
        #self.print_dijkstra_map()
        return maxDist
        
    def sumElementsFromStrPath(self,
                               combis: Combinations,
                               path: List[str],
                               attr: str,
                               res: T) -> T:
        pos = "start"
        for elem in path:
            res += getattr(combis[pos][elem], attr)
            pos = elem
        return res

    def getDistanceFromStrPath(self,
                               combis: Combinations,
                               path: List[str]) -> int:
        return self.sumElementsFromStrPath(combis, path, "distance", 0)

    def getPathFromStrPath(self,
                           combis: Combinations,
                           path: List[str]) -> List[Point]:
        return self.sumElementsFromStrPath(combis, path, "path", [])


def main(lines: List[str]):
    maze = MazeGame(lines)
    res = maze.dijkstra_path_key(maze.startPos, maze.endPos)
    print(res)
    # print(len(res))

    #t = turtle_mode.Turtle_mode(maze.gsx, maze.gsy, maze.numKeys)
    #t.play_maze_manual(maze.map, res, maze.startPos)


def getPath(lines: List[str]) -> int:
    maze = MazeGame(lines)
    return maze.dijkstra_path_key(maze.startPos, maze.endPos)


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
    sys.setrecursionlimit(99999)
    unit_test()

    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
