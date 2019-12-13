#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections

from sympy import Point, pi
from sympy.geometry import Line, Segment


class Event(NamedTuple):
    num: int
    ev: str


def print_map(lines: List[str], asts_count: List[int]):
    height = len(lines)
    width = len(lines[0])
    ind = 0
    for line in lines:
        for elem in list(line):
            if elem == '.':
                print(elem, end='')
            else:
                print(asts_count[ind], end='')
                ind += 1
        print()


def find_max_asts(center: Point, asteroids: List[Point]) -> int:
    angle_line = Line(center, Point(center.x, center.y + 200))
    arr = []
    for elem in asteroids:
        if elem == center:
            continue
        seg = Segment(center, elem)
        angle = float(seg.angle_between(angle_line))
        if elem.x < center.x:
            angle = float(pi - angle - pi)
        seg_len = float(seg.length)
        nt = (seg_len, elem)
        t = [elem[1] for elem in arr if elem[0] == angle]
        if t:
            t[0].append(nt)
        else:
            arr.append((angle, [nt]))


    arr.sort(key=lambda x: x[0], reverse=True)
    for elem in arr:
        elem[1].sort(key=lambda x: x[0])

    res = None
    i = counter = 0
    while counter < 200:
        plans = arr[i % len(arr)][1]
        if plans:
            res = plans.pop(0)[1]
            print(counter + 1, int(res.x / 2), int(res.y / 2))
        else:
            #del arr[i % len(arr)]
            counter -= 1
        i += 1
        counter += 1
    return res


def main(lines: List[str]):
    y = 0
    asteroids = []
    for line in lines:
        x = 0
        for elem in list(line):
            point = Point(x + 1, y + 1)
            if elem == "#":
                asteroids.append(point)
            x += 2
        y += 2

    # print(len(asteroids))

    center = Point(23 * 2 + 1, 29 * 2 + 1)
    #center = Point(8 * 2 + 1, 3 * 2 + 1)
    #center = Point(11 * 2 + 1, 13 * 2 + 1)
    #print(asteroids)
    res = find_max_asts(center, asteroids)
    # print(find_max_asts(Point(11, 17), asteroids.copy()))
    print("200th ast at pos:", int(res.x / 2) * 100 + int(res.y / 2))


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
