#!/usr/bin/env python3

from __future__ import annotations
import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections


class Planet(NamedTuple):
    name: str
    orbits: List[Planet]

    def __eq__(self, n: str):
        return n == self.name


def get_planet(name: str, planets: List[Planet]) -> Planet:
    try:
        ind = planets.index(name)
        return planets[ind]
    except ValueError:
        plan = Planet(name, [])
        planets.append(plan)
        return plan

def walk_recur(plan: Planet, suborbs: int):
    s = suborbs
    for sub_plan in plan.orbits:
        s += walk_recur(sub_plan, suborbs + 1)
    return s

def main(lines: List[str]):
    planets: List[Planet] = []
    for line in lines:
        orbs = line.split(")")
        p1 = get_planet(orbs[0], planets)
        p2 = get_planet(orbs[1], planets)
        p1.orbits.append(p2)

    com = planets[planets.index("COM")]
    res = walk_recur(com, 0)
    print(res)


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
