#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections

from sympy import Point
from sympy.geometry import Line


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


angle_line = Line(Point(0, 0), Point(1, 100))


def find_max_asts(center: Point, asteroids: List[Point]) -> int:
    s = set()
    for elem in asteroids:
        if elem == center:
            continue
        angle = Line(center, elem).angle_between(angle_line)
        s.add(angle)
    return len(s)


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

    #print(len(asteroids))
    asts_count = [find_max_asts(elem, asteroids) for elem in asteroids]

    res = max(asts_count)
    pos_res = asteroids[asts_count.index(res)]
    print_map(lines, asts_count)
    # print(find_max_asts(Point(11, 17), asteroids.copy()))
    print("max asteroids:", res, "at pos Y:", int(pos_res.y / 2), "X:", int(pos_res.x / 2))


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
