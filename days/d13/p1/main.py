#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple, TextIO
from inspect import signature
import collections


class Event(NamedTuple):
    num: int
    ev: str


class Mach2:

    def __init__(self, inp: List[int], mem_str: str, file: TextIO = sys.stdout):
        self._input = inp
        self._mem = [int(x) for x in mem_str.split(',')]
        self._mem.extend([0] * 10000)
        self._counter = 0
        self._relative_base = 0
        self._file_output = file

    def _add(self, a1, a2, pos):
        self._mem[pos] = a1 + a2

    def _mul(self, a1, a2, pos):
        self._mem[pos] = a1 * a2

    def _inp(self, a1):
        val = self._input.pop(0)
        # val = int(input())
        self._mem[a1] = val

    def _out(self, a1):
        print(a1, file=self._file_output)

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
        # print("mem[0]:", mem[0])
        exit()

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


def main(lines: List[str]):
    with open("machineOutput.txt", "r+") as f:
        breakout_lines = f.readlines()
        if not breakout_lines:
            print("getting breakout game")
            m = Mach2([], lines[0], f)
            m.run()
            f.flush()
            breakout_lines = f.readlines()

    inp = [int(line) for line in breakout_lines]
    print(inp)
    grid = []
    gridsize_x = 45
    gridsize_y = 24
    for i in range(0, gridsize_y):
        grid.append([0] * gridsize_x)

    count = 0
    for i in range(0, len(inp), 3):
        grid[inp[i + 1]][inp[i]] = inp[i + 2]
        if inp[i + 2] == 0:
            grid[inp[i + 1]][inp[i]] = "."
        if inp[i + 2] == 2:
            count += 1


    for y in range(0, gridsize_y):
        for x in range(0, gridsize_x):
            print(grid[y][x], end=' ')
        print()

    print(inp.count(2), count)

def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
