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


@dataclass
class Possibility:
    path: str
    dist: int
    id: int
    pos: List[str]
    robot: List[int]


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

    badPath: Path
    isAnnoyingSpecialCase: bool
    atInd: List[int]
    startPos: List[Point()]
    numKeys: int
    keys: List[str]
    numBots :int

    def getPoint(self, p: Point) -> str:
        # on enlève la condition car On vit dans le Danger. pis y'a des murs partout
        # if p.x < 0 or p.y < 0 or p.x >= self.gsx or p.y >= self.gsy:
        #    return '#'
        return self.map[p.y * self.gsx + p.x]

    def getPointFromIndex(self, index: int) -> Point:
        return Point(index % self.gsx, int(index / self.gsx))

    def get_map_pos(self, map: List[int], pos: Point) -> int :
        return map[pos.y * self.gsx + pos.x]  


    def __init__(self, lines: List[str]):
        self.gsx = len(lines[0])
        self.gsy = len(lines)
        self.map = "".join(lines)
        self.numBots = self.map.count('@')

        ind  = -1
        self.atInd = []
        self.startPos = []
        self.numKeys = []
        self.keys = []
        for _ in range(self.numBots):
            ind = self.map.index('@', ind + 1)
            self.atInd.append(ind)
            self.startPos.append(self.getPointFromIndex(ind))


        self.numKeys = len([c for c in self.map if ord(c)
                            in range(ord('a'), ord('z')+1)])


        self.isAnnoyingSpecialCase = False
        if self.numBots == 1:
            st = self.startPos[0]
            if (self.getPoint(st + Point(0,1)) == "." and
                self.getPoint(st + Point(-1,0)) == "." and 
                self.getPoint(st + Point(-1,1)) == "."):
                self.isAnnoyingSpecialCase = True

        self.dijkstra_map = [-2 if x == '#' else -1 for x in self.map]
        if self.isAnnoyingSpecialCase:
            self.dijkstra_map[self.atInd[0]] = -2


        self.directions = [Point(-1, 0), Point(0, -1),
                           Point(1, 0), Point(0, 1)]
        self.badPath = Path(999, [], [])



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
            wallInd = -1 if searchedPos.x < startPos.x else 1
            map[self.atInd[0] - wallInd] = -2
            if startPos == self.startPos[0]:
                map[self.atInd[0] + wallInd] = -2

        self.dijkstra_recursive_mapping(map, startPos, 0)
        maxDist = self.get_map_pos(map, searchedPos)
        if maxDist == -1:
            return self.badPath
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


    def getCombisPart(self, startPos: Point) -> Combinations:
        keys = []
        keyPos = []
        combis: Combinations = {'@': {}}
        for p1 in range(self.numKeys):
            currChar = chr(ord('a')+p1)
            #print("start", currChar)
            keyInd = self.map.index(currChar)
            pos = self.getPointFromIndex(keyInd)

            path = self.dijkstra_path_key(startPos, pos)
            if path == self.badPath:
                continue
            keys.append(currChar)
            keyPos.append(pos)
            combis['@'][currChar] = path

        for char in keys:
            combis[char] = {}

        for x in range(len(keys)):
            xChar = keys[x]
            for y in range(x+1, len(keys)):
                yChar = keys[y]
                #print(xChar, yChar)
                nPath = self.dijkstra_path_key(keyPos[x], keyPos[y])
                combis[xChar][yChar] = nPath

                p2 = deepcopy(nPath)
                p2.path.reverse()
                p2.path = [x.reverse() for x in p2.path]
                combis[yChar][xChar] = p2


        #f = open("combinations_object.py", 'wb')
        #pickle.dump(combis, f)
        # print(combis)
        return combis


    def getAllCombis(self) -> List[Combinations]:
        return [ self.getCombisPart(start) for start in self.startPos]


    def hashNum(self, key: str, numComb: int):
        return pow(2,(ord(key)-96) * (numComb+1))
        #96 = ord('a') - 1

    def tryFasterSolution(self, combisList: List[Combinations]) -> Tuple(int, List[Tuple(int, List[Point])]):
        #ind = 123456789abcd
        initialPos = ['@']*self.numBots
        possibilities = {}

        for numComb, combis in enumerate(combisList):
            for key, elem in combis['@'].items():
                if combis['@'][key].doors:
                    continue
                nPos = copy(initialPos)
                nPos[numComb] = key
                
                idNum = self.hashNum(key, numComb)
                p = Possibility([key], elem.distance, idNum, nPos, [numComb])
                possibilities[str(idNum)+"".join(nPos)] = p

        for _ in range(self.numKeys - 1):
            nextStepPossibilities = {}
            for poss in possibilities.values():
                for numComb, combis in enumerate(combisList):
                    for key, elem in combis[poss.pos[numComb]].items():
                        if key in poss.path or any(door not in poss.path for door in elem.doors):
                            continue
                        nPos = copy(poss.pos)
                        nPos[numComb] = key
                        nDist = poss.dist + elem.distance
                        nIdNum = poss.id + self.hashNum(key, numComb)
                        nId = str(nIdNum)+"".join(nPos)
                        existingKey = nextStepPossibilities.get(nId)
                        if existingKey and existingKey.dist <= nDist:
                            continue
                        p = Possibility(poss.path + [key], 
                                        nDist, nIdNum, nPos,
                                        poss.robot + [numComb])
                        nextStepPossibilities[nId] = p
            possibilities = nextStepPossibilities


        #print(possibilities)
        res = min(possibilities.values(), key=lambda val:val.dist)
        print("dist:", res.dist)
        #print("path:", res.path)

        path = []
        pos = ["@"]*self.numBots
        for indBot, elem in enumerate(res.path):
            bot = res.robot[indBot]
            part = combisList[bot][pos[bot]][elem].path
            path.append((bot, part))
            pos[bot] = elem
        return (res.dist, path)

def getCombisFromFile():
    fname = "combinations_object_otherinput.py"
    #fname = "combinations_object_big_dijkstra.py"
    f = open(fname, "rb")
    combis = pickle.load(f)
    return combis

def main(lines: List[str]):
    maze = MazeGame(lines)

    combis = maze.getAllCombis()
    #combis = getCombisFromFile()
    _, path = maze.tryFasterSolution(combis)

    t = turtle_mode.Turtle_mode(maze.gsx, maze.gsy, maze.numKeys, maze.numBots)
    t.play_maze_manual(maze.map, path, maze.startPos)


def getPath(lines: List[str]):
    maze = MazeGame(lines)
    #assert(maze.getPoint(maze.startPos) == '@')
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
    unit_test()
    
    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
