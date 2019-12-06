#!/usr/bin/env python3

from __future__ import annotations
import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections


class Planet(NamedTuple):
    name: str
    orbits: List[Planet]
    orbiting: List[Planet]

    def __eq__(self, n: str):
        return n == self.name


def get_planet(name: str, planets: List[Planet]) -> Planet:
    try:
        ind = planets.index(name)
        return planets[ind]
    except ValueError:
        plan = Planet(name, [], [])
        planets.append(plan)
        return plan


def walk_recur(plan: Planet, suborbs: int, previous: Planet) -> int:
    #print(plan.name)
    if plan.name == "SAN":
        return suborbs + 1

    for elem in plan.orbits:
        res = walk_recur(elem, suborbs + 1, plan)
        if res != -1:
            return res

    if len(plan.orbiting) != 0 and previous != plan.orbiting[0]:
        res = walk_recur(plan.orbiting[0], suborbs + 1, plan)
        if res != -1:
            return res

    return -1


def main(lines: List[str]):
    planets: List[Planet] = []
    for line in lines:
        orbs = line.split(")")
        p1 = get_planet(orbs[0], planets)
        p2 = get_planet(orbs[1], planets)
        p1.orbits.append(p2)
        p2.orbiting.append(p1)

    com = planets[planets.index("YOU")]
    res = walk_recur(com, 0, com)
    print(res - 3)

def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
