#!/usr/bin/env python3

from __future__ import annotations

import sys
import copy
import time
import curses
from dataclasses import dataclass
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple, TextIO
from inspect import signature
import collections
import turtle


class Event(NamedTuple):
    num: int
    ev: str


class Mach2:

    def __init__(self, inp: List[int], mem_str: str):
        self._input = inp
        self._mem = [int(x) for x in mem_str.split(',')]
        self._mem.extend([0] * 10000)
        self._counter = 0
        self._relative_base = 0
        self._output = []
        self._ended = False

    def ended(self) -> bool:
        return self._ended

    def add_input(self, n: int):
        self._input.append(n)

    def _add(self, a1, a2, pos):
        self._mem[pos] = a1 + a2

    def _mul(self, a1, a2, pos):
        self._mem[pos] = a1 * a2

    def _inp(self, a1):
        # print(self._output)
        self._output = []
        val = self._input.pop(0)
        # val = int(input())
        self._mem[a1] = val

    def _out(self, a1):
        self._output.append(a1)
        # print(a1, file=self._file_output)

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
        self._ended = True
        # print("end program")
        # print("mem[0]:", mem[0])
        # exit()

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

    def run(self) -> List[int]:
        self._output = []
        mem = self._mem
        while self._counter < len(mem):
            op = mem[self._counter] % 100
            method = self.opcodes[op].get("meth")
            if op == 3 and not self._input:
                return self._output

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

            if self._ended:
                self._ended = False
                return self._output


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)


class MazeGame:
    gridsize_x: int
    gridsize_y: int

    mac: Mach2
    droid_pos: Point
    oxy_pos: Point

    keys: List[str]
    directions: List[Point]
    screen: turtle.Screen
    canvas: turtle.ScrolledCanvas
    display_mul: int
    operating: bool

    backtrack: List[int]
    solutions: List[int]

    def __init__(self, gsx: int, gsy: int, m: Mach2):
        self.gridsize_x = gsx
        self.gridsize_y = gsy
        self.mac = m
        self.droid_pos = Point(int(gsy / 2), int(gsx / 2))
        self.oxy_pos = Point(-1, -1)

        self.keys = ["Down", "Up", "Left", "Right"]
        self.directions = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]

        self.screen = turtle.Screen()
        self.canvas = turtle.getcanvas()
        turtle.setup(1900, 1000, 0, 0)
        self.display_mul = 20
        self.color_ratio = 10

        self.santa_icon = "./santa_bot.gif"
        self.oxygen_icon = "./OxygenCircle.gif"
        self.screen.addshape(self.santa_icon)
        self.screen.addshape(self.oxygen_icon)
        self.screen.bgcolor("#010026")
        turtle.shape(self.santa_icon)
        turtle.speed("fast")
        turtle.penup()
        self.set_turtle_pos(self.droid_pos)

        self.operating = False
        self.backtrack = [1, 0, 3, 2]
        self.solutions = []
        self.max_iter = 0

    def set_turtle_pos(self, pos: Point):
        turtle.setpos((pos.x - self.gridsize_x / 2) * self.display_mul,
                      (pos.y - self.gridsize_y / 2) * self.display_mul)

    def draw_rectangle(self, pos: Point, col, ratio: int):
        bx = pos.x - self.gridsize_x / 2
        by = -pos.y + self.gridsize_x / 2
        self.canvas.create_rectangle((bx - ratio) * self.display_mul, (by - ratio) * self.display_mul,
                                     (bx + ratio) * self.display_mul, (by + ratio) * self.display_mul, fill=col)

    def display_victory(self) -> int:
        print("O2 machine found!")

    def move(self, direction: int):
        if self.operating:
            return
        self.operating = True

        self.mac.add_input(direction + 1)
        out = self.mac.run()
        out = out[0]
        npos = self.droid_pos + self.directions[direction]

        if out == 2:
            self.droid_pos = npos
            self.oxy_pos.x = self.droid_pos.x
            self.oxy_pos.y = self.droid_pos.y
            self.set_turtle_pos(npos)
            turtle.shape(self.oxygen_icon)
            turtle.stamp()
            turtle.shape(self.santa_icon)
            self.display_victory()
        if out == 0:
            self.draw_rectangle(npos, "white", 0.45)
        if out == 1:
            self.set_turtle_pos(npos)
            self.droid_pos = npos
        self.operating = False
        return out

    def play_maze_manual(self):
        for i in range(0, len(self.keys)):
            self.screen.onkey(lambda i=i: self.move(i), self.keys[i])
        self.screen.listen()
        self.screen.mainloop()

    def play_maze_color_p2(self, iteration: int, dir: int):
        res = self.move(dir)
        if res == 0:
            return
        self.max_iter = max(iteration, self.max_iter)
        col = "#{:03X}{:03X}000".format(iteration * self.color_ratio, 4095 - iteration * self.color_ratio)
        self.draw_rectangle(self.droid_pos, col, 0.5)

        for i in range(0, 4):
            if i == self.backtrack[dir]:
                continue
            self.play_maze_color_p2(iteration + 1, i)
        self.move(self.backtrack[dir])

    def play_maze_auto(self, iteration: int, dir: int) -> bool:
        res = self.move(dir)
        if res == 0:
            return True
        if res == 2:
            for i in range(0, 4):
                self.play_maze_color_p2(1, i)
            return False

        for i in range(0, 4):
            if i == self.backtrack[dir]:
                continue
            if not self.play_maze_auto(iteration + 1, i):
                return False
        self.move(self.backtrack[dir])
        return True


def main(lines: List[str]):
    m = Mach2([], lines[0])
    maze = MazeGame(60, 60, m)
    # maze.play_maze_manual()
    # turtle.tracer(0, 0)

    input()
    for i in range(0, 4):
        maze.play_maze_auto(0, i)

    print(maze.max_iter)
    turtle.update()
    maze.screen.mainloop()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
