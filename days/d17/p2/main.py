#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, NamedTuple, Tuple
from copy import copy
import turtle_mode

from intcode import Machine


class Event(NamedTuple):
    num: int
    ev: str


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)


class MazeGame:
    gsx: int
    gsy: int

    mac: Machine
    map: List[int]
    droid_pos: Point
    oxy_pos: Point

    directions: List[Point]
    operating: bool

    intersections: List[Point]
    backtrack: List[int]
    solutions: List[int]

    def getPoint(self, p: Point) -> int:
        if p.x < 0 or p.y < 0 or p.x >= self.gsx or p.y >= self.gsy:
            return ord('.')
        return self.map[p.y * self.gsx + p.x]

    def __init__(self, m: Machine):
        self.mac = m
        out = self.mac.run()
        self.gsx = out.index(ord("\n"))
        self.gsy = int(len(out) / self.gsx)
        # print map
        # for i in out:
        #    print(chr(i), end="")

        self.map = [i for i in out if i != ord('\n')]

        ind_droid = self.map.index(ord('^'))
        self.droid_pos = Point(ind_droid % self.gsx, int(ind_droid / self.gsx))

        self.directions = [Point(-1, 0), Point(0, -1),
                           Point(1, 0), Point(0, 1)]

        self.operating = False
        self.backtrack = [1, 0, 3, 2]
        self.solutions = []
        self.intersections = []
        self.max_iter = 0
        # self.turtle_init()

    def get_intersections(self):
        for y in range(0, self.gsy):
            for x in range(0, self.gsx):
                curr = Point(x, y)
                if self.getPoint(curr) == ord("."):
                    continue
                is_inter = True
                for elem in self.directions:
                    if self.getPoint(curr + elem) == ord("."):
                        is_inter = False
                if is_inter:
                    self.intersections.append(curr)
        # print(self.intersections)

    def testDirection(self, pos: Point, dirIndex: int, dir: int) -> int:
        if self.getPoint(pos + self.directions[(dirIndex + dir) % 4]) == ord('#'):
            return dir
        return 0

    def get_paths(self) -> str:
        startInd = self.map.index(ord("^"))
        startPos = Point(startInd % self.gsx, startInd // self.gsy - 2)
        # print(startPos)

        pos = startPos
        solution = []
        dirIndex = self.directions.index(Point(0, -1))
        moves = 0

        npos = pos
        currDir = self.directions[dirIndex % 4]
        while True:
            npos += currDir
            if self.getPoint(npos) == ord('.'):
                # print(solution)
                solution.append(str(moves))
                moves = -1
                npos = npos - currDir

                r = 0
                r = self.testDirection(npos, dirIndex, -1)
                if r == 0:
                    r = self.testDirection(npos, dirIndex, 1)

                if r == 0:
                    #print("ended movement")
                    st = ",".join(solution[1:])
                    #print(st, len(st))
                    return st
                else:
                    dirIndex += r
                    charDir = 'L' if r == -1 else 'R'
                    solution.append(charDir)
                    currDir = self.directions[dirIndex % 4]
            moves += 1

        currDir = Point(0, 1)


def check_end_path(path: str, patterns: List[str]) -> List[List[str]]:
    if len(path) > 20:
        return False
    res = not any(t not in ['A', 'B', 'C', ','] for t in list(path))
    if res:
        print("SOLUTION FOUND!", path, patterns)
        return [path] + patterns
    return []


def check_last_pattern(path: str, patterns: List[str]) -> List[List[str]]:
    start = 0
    while path[start] in ['A', 'B', 'C', ',']:
        start += 1
    end = start
    while path[end] not in ['A', 'B', 'C']:
        end += 1
    end -= 1
    part = path[start:end]
    nst = path.replace(part, 'C')
    return check_end_path(nst, patterns + [part])


def replace_pattern(path: str, part: str, patterns: List[str]) -> List[List[str]]:
    nst = path.replace(part, chr(ord('A') + len(patterns)))
    return convert_path(nst, patterns + [part])


def convert_path(path: str, patterns: List[str] = []) -> List[List[str]]:
    if len(patterns) == 2:
        return check_last_pattern(path, patterns)

    indices = [0] + [i+1 for i, a in enumerate(path) if a == ',']
    for i in indices:
        if path[i] in ['A', 'B', 'C']:
            continue

        # try all patterns len
        start = i
        for pattLen in range(2, 11):
            end = start
            try:
                for _ in range(pattLen):
                    end = path.index(",", end + 1)
            except ValueError:
                end = len(path)

            if end - start > 20 or path[end-1] in ['A', 'B', 'C']:
                break
            res = replace_pattern(path, path[start:end], patterns)
            if res:
                return res
            if end == len(path):
                break
    return False

def machine_solve(patterns: List[List[str]], lines: List[str]):
    inp = "\n".join(patterns + ["n"])
    #print("input machine:", inp)
    inp = [ord(i) for i in inp]
    inp += [ord('\n')]
    nLines = "2" + lines[0][1:]
    m = Machine(inp, nLines)
    res = m.run()
    print("res:", res[-1])


def main(lines: List[str]):
    m = Machine([], lines[0])

    #out = m.run()
    # for elem in out:
    #    print(chr(elem), end="")
    # exit()

    maze = MazeGame(m)
    maze.get_intersections()
    path = maze.get_paths()
    #path = "R,8,L,10,R,8,R,12,R,8,L,8,L,12,R,8,L,10,R,8,L,12,L,10,L,8,R,8,L,10,R,8,R,12,R,8,L,8,L,12,L,12,L,10,L,8,L,12,L,10,L,8,R,8,L,10,R,8,R,12,R,8,L,8,L,12"
    patterns = convert_path(path)
    machine_solve(patterns, lines)


    t = turtle_mode.Turtle_mode(maze.gsx, maze.gsy)
    t.play_maze_manual(maze.map, path, patterns)
    #maze.play_maze_manual()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
