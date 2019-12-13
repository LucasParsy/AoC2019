#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections
from math import cos, sin, radians
import turtle
import time


class Point:
    x: int
    y: int
    color: int

    def __init__(self, nx, ny):
        self.x = nx
        self.y = ny
        self.color = 0


class Machine:

    def __init__(self, inp: List[int], mem_str: str):
        self.ended = False

        self._output = None
        self._input = inp
        self._mem = [int(x) for x in mem_str.split(',')]
        self._mem.extend([0] * 10000)
        self._counter = 0
        self._relative_base = 0

    def add_input(self, i: int):
        self._input.append(i)

    def _add(self, a1, a2, pos):
        self._mem[pos] = a1 + a2

    def _mul(self, a1, a2, pos):
        self._mem[pos] = a1 * a2

    def _inp(self, a1):
        val = self._input.pop(0)
        # val = int(input())
        self._mem[a1] = val

    def _out(self, a1):
        self._output = a1
        # print(a1)

    def _nz(self, a1, a2):
        if a1 != 0:
            return a2

    def _ez(self, a1, a2):
        if a1 == 0:
            return a2

    def _lt(self, a1, a2, a3):
        self._mem[a3] = 1 if a1 < a2 else 0

    # def gt(mem: List[int], a1, a2, a3):
    #    mem[a3] = 1 if a1 > a2 else 0

    def _eq(self, a1, a2, a3):
        self._mem[a3] = 1 if a1 == a2 else 0

    def _rb(self, a1):
        self._relative_base += a1

    def _ex(self):
        print("end program")
        self.ended = True
        # print("mem[0]:", mem[0])
        #exit()

    opcodes = {
        1: {"meth": _add, "mem_params": [0, 0, 1]},
        2: {"meth": _mul, "mem_params": [0, 0, 1]},
        3: {"meth": _inp, "mem_params": [1]},
        4: {"meth": _out, "mem_params": [0]},
        5: {"meth": _nz, "mem_params": [0, 0]},
        6: {"meth": _ez, "mem_params": [0, 0]},
        7: {"meth": _lt, "mem_params": [0, 0, 1]},
        8: {"meth": _eq, "mem_params": [0, 0, 1]},
        9: {"meth": _rb, "mem_params": [0]},
        99: {"meth": _ex, "mem_params": []},
    }

    def run(self):
        mem = self._mem
        while self._counter < len(mem):
            op = mem[self._counter] % 100
            method = self.opcodes[op].get("meth")
            mem_params = self.opcodes[op].get("mem_params")
            num_params = len(mem_params)
            params = mem[self._counter + 1: self._counter + 1 + num_params]

            inst = str(mem[self._counter])
            modes_list = [int(x) for x in list(inst.zfill(num_params + 2)[:-2])]
            modes_list.reverse()
            for u in range(0, len(modes_list)):
                if modes_list[u] == 0 and mem_params[u] != 1:
                    params[u] = mem[params[u]]
                elif modes_list[u] == 2:
                    if mem_params[u] != 1:
                        params[u] = mem[params[u] + self._relative_base]
                    else:
                        params[u] = params[u] + self._relative_base

            new_pos = method(self, *params)
            if isinstance(new_pos, int):
                self._counter = new_pos
            else:
                self._counter += num_params + 1

            if self._output is not None:
                res = self._output
                self._output = None
                return res


def main(lines: List[str]):
    m = Machine([], lines[0])
    angle = 0
    pos = Point(0, 0)
    painted = set()
    start_point = Point(pos.x, pos.y)
    start_point.color = 1
    painted.add(start_point)

    turtle.speed("fastest")
    turtle.shape("turtle")
    turtle.setheading(90)
    turtle.penup()

    while not m.ended:
        tile = [elem for elem in painted if elem.x == pos.x and elem.y == pos.y]
        if not tile:
            tile = Point(pos.x, pos.y)
            painted.add(tile)
        else:
            tile = tile[0]

        color = tile.color
        m.add_input(color)
        ncol = m.run()
        if ncol == 1:
            turtle.pendown()
            turtle.dot(3, "black")
            turtle.penup()
        tile.color = ncol
        direction = m.run()
        angle += 90 if direction == 1 else -90
        angle = angle % 360
        pos.y += int(cos(radians(angle)))
        pos.x += int(sin(radians(angle)))
        turtle.setheading(360 - angle + 90)
        turtle.forward(7)

    turtle.hideturtle()
    turtle.done()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
