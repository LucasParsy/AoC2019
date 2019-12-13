#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections
from math import cos, sin, radians
import turtle
import time


class Planet:
    x: int
    y: int
    z: int

    vel_x: int
    vel_y: int
    vel_z: int

    def __init__(self, st: str):
        nums = [int(t.strip()[2:]) for t in st[1:-1].split(',')]

        self.x = nums[0]
        self.y = nums[1]
        self.z = nums[2]

        self.vel_x = self.vel_y = self.vel_z = 0

    def get_direction(self, x: int, y: int) -> int:
        if x == y:
            return 0
        return 1 if x < y else -1

    def step_gravity(self, other):
        direction = self.get_direction(self.x, other.x)
        self.vel_x += direction
        other.vel_x -= direction

        direction = self.get_direction(self.y, other.y)
        self.vel_y += direction
        other.vel_y -= direction

        direction = self.get_direction(self.z, other.z)
        self.vel_z += direction
        other.vel_z -= direction

    def step_velocity(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z

    def total_energy(self) -> int:
        pot = abs(self.x) + abs(self.y) + abs(self.z)
        kin = abs(self.vel_x) + abs(self.vel_y) + abs(self.vel_z)
        return pot * kin


def main(lines: List[str]):
    planets = []
    for line in lines:
        planets.append(Planet(line))

    for i in range(0, 1000):
        for j in range(0, len(planets)):
            for h in range(j + 1, len(planets)):
                planets[j].step_gravity(planets[h])

        for p in planets:
            p.step_velocity()

    res = 0
    for p in planets:
        res += p.total_energy()
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
