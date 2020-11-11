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
import itertools

from Point import Point
import turtle_mode

@dataclass
class Path:
    distance: int
    path: List[Point]
    doors: List[str]


# typings
T = TypeVar('T', int,  List[Point],  List[str])
Combinations = Dict[str, Dict[str, Path]]

badPath = Path(999, [], [])
badPoint = Point(2, 2)

class MazeGame:
    gsx: int
    gsy: int

    map: List[str]

    directions: List[Point]

    backtrack: List[int]
    badPath: Path
    wallsChar: List[str]
    isAnnoyingSpecialCase: bool
    atInd: int

    def getPoint(self, p: Point) -> str:
        # on enlève la condition car On vit dans le Danger. pis y'a des murs partout
        # if p.x < 0 or p.y < 0 or p.x >= self.gsx or p.y >= self.gsy:
        #    return '#'
        return self.map[p.y * self.gsx + p.x]

    def getPointFromIndex(self, index: int) -> Point:
        return Point(index % self.gsx, int(index / self.gsx))

    def get_map_pos(self, map: List[int], pos: Point) -> int :
        return map[pos.y * self.gsx + pos.x]  


    def __init__(self, lines: List[str], isSpecialCase=False):
        self.gsx = len(lines[0])
        self.gsy = len(lines)
        self.map = "".join(lines)

        self.isAnnoyingSpecialCase = isSpecialCase
        self.dijkstra_map = [-2 if x == '#' else -1 for x in self.map]

        self.atInd = self.map.index('@')
        if self.isAnnoyingSpecialCase:
            self.dijkstra_map[self.atInd] = -2

        self.startPos = self.getPointFromIndex(self.atInd)
        self.numKeys = len([c for c in self.map if ord(c)
                            in range(ord('a'), ord('z')+1)])

        self.directions = [Point(-1, 0), Point(0, -1),
                           Point(1, 0), Point(0, 1)]

        self.badPath = Path(999, [], [])
        # self.turtle_init()



    def dijkstra_recursive_mapping(self, map: List[int], currPoint: Point, distance: int):
        pos = currPoint.y * self.gsx + currPoint.x
        if map[pos] != -1:
            return
        map[pos] = distance
        for dir in self.directions:
            self.dijkstra_recursive_mapping(map, currPoint + dir, distance+1)
            

    def dijkstra_path_key(self, startPos: Point, searchedPos: Point) -> Path:
        map = copy(self.dijkstra_map)
        if self.isAnnoyingSpecialCase:
            pos = startPos.y * self.gsx + startPos.x
            map[pos] = -1
            wallInd = -1 if searchedPos.x < self.startPos.x else 1
            map[self.atInd - wallInd] = -2
            if startPos == self.startPos:
                map[self.atInd + wallInd] = -2

        self.dijkstra_recursive_mapping(map, startPos, 0)
        maxDist = self.get_map_pos(map, searchedPos)
        path = []
        doors = []
        dist = maxDist
        pos = searchedPos

        while(dist != 0):
            dist -= 1
            for dir in self.directions:
                nPos = pos + dir
                if self.get_map_pos(map, nPos) == dist:
                    pos = nPos
                    path.append(dir.reverse())
                    c = self.getPoint(nPos)
                    if ord(c) in range(ord('A'), ord('Z')+1):
                        doors.append(chr(ord(c)+32))
                    break
        path.reverse()
        doors.reverse()
        return Path(maxDist, path, doors)
    
    def sortCombiList(self, combis: Combinations, index: str):
        return {k: v for k, v in sorted(combis[index].items(), key=lambda item: item[1].distance)}

    def getAllCombis(self) -> List[Point]:
        alphabet = [chr(x) for x in range(ord('a'), ord('z')+1)]
        keyPos = []
        combis: Combinations = {'start': {}}
        for p1 in range(self.numKeys):
            currChar = chr(ord('a')+p1)
            #print("start", currChar)
            keyInd = self.map.index(currChar)
            pos = self.getPointFromIndex(keyInd)
            keyPos.append(pos)

            path = self.dijkstra_path_key(self.startPos, pos)
            combis['start'][currChar] = path
        combis['start'] = self.sortCombiList(combis, 'start')

        for x in range(self.numKeys):
            xChar = alphabet[x]
            combis[xChar] = {}
            for y in range(self.numKeys):
                yChar = alphabet[y]
                if y < x:
                    revComb = combis[yChar][xChar]
                    nPath = deepcopy(revComb)
                    nPath.path.reverse()
                    nPath.path = [x.reverse() for x in nPath.path]
                    combis[xChar][yChar] = nPath
                elif y == x:
                    continue
                else:
                    #print(xChar, yChar)
                    nPath = self.dijkstra_path_key(keyPos[x], keyPos[y])
                    combis[xChar][yChar] = nPath
            combis[xChar] = self.sortCombiList(combis, xChar)
        f = open("combinations_object.py", 'wb')
        pickle.dump(combis, f)
        # print(combis)
        return combis

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


    def tryFasterSolution(self, combis: Combinations) -> List[Point]:
        asciiA = ord('a') - 1
        possibilities = {}
        for key, elem in combis['start'].items():
            idNum = pow(2,ord(key)-asciiA)
            possibilities[str(idNum)+key] = ([key], elem.distance, idNum)

        for _ in range(self.numKeys - 1):
            nextStepPossibilities = {}
            for id, poss in possibilities.items():
                path = poss[0]
                for key, elem in combis[path[-1]].items():
                    if key in path or any(door not in path for door in elem.doors):
                        continue
                    nDist = poss[1]+ elem.distance
                    nIdNum = poss[2] + pow(2, ord(key)-asciiA)
                    nId = str(nIdNum)+key
                    existingKey = nextStepPossibilities.get(nId)
                    if existingKey and existingKey[1] <= nDist:
                        continue
                    nextStepPossibilities[nId] = (path + [key], nDist, nIdNum)
            possibilities = nextStepPossibilities
        
        
        #print(possibilities)
        res = min(possibilities.values(), key=lambda val:val[1])
        print("dist:", res[1])
        print("path:", res[0])
        return self.getPathFromStrPath(combis, res[0])

def getCombisFromFile():
    fname = "combinations_object_otherinput.py"
    #fname = "combinations_object_big_dijkstra.py"
    f = open(fname, "rb")
    combis = pickle.load(f)
    #l = f.readline()
    #combis = eval(l)
    return combis

def main(lines: List[str]):
    maze = MazeGame(lines, True)

    combis = maze.getAllCombis()
    #combis = getCombisFromFile()
    res = maze.tryFasterSolution(combis)

    #res = maze.path_map(Point(2, 2), maze.startPos, [], [])
    # print(len(res))

    #res = [Point(0,1)]
    solution = ['start', 'n', 'f', 'i', 'l', 'x', 'p', 'z', 'c', 'r', 'm', 't',
                'a', 'k', 'd', 'v', 'j', 'e', 'w', 'y', 'q', 'o', 's', 'u', 'b', 'g', 'h']
    #print(maze.getDistanceFromStrPath(combis, solution[1:])) #5070
    #res = maze.getPathFromStrPath(combis, solution[1:])

    t = turtle_mode.Turtle_mode(maze.gsx, maze.gsy, maze.numKeys)
    t.play_maze_manual(maze.map, res, maze.startPos)


def getPath(lines: List[str]):
    maze = MazeGame(lines)
    assert(maze.getPoint(maze.startPos) == '@')
    combis = maze.getAllCombis()
    return maze.tryFasterSolution(combis)

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
            assert(len(res) == expected)

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
    unit_test()
    
    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
