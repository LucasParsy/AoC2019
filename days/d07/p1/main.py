#!/usr/bin/env python3

import sys
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections


class Event(NamedTuple):
    num: int
    ev: str


class Machine:
    def __init__(self, inp: List[int], mem_str: str):
        self.output = -1
        self.input = inp
        self.mem = [int(x) for x in mem_str.split(',')]

    def add(self, mem: List[int], a1, a2, pos):
        mem[pos] = a1 + a2

    def mul(self, mem: List[int], a1, a2, pos):
        mem[pos] = a1 * a2

    def inp(self, mem: List[int], a1):
        # val = int(input())
        val = self.input.pop()
        mem[a1] = val

    def out(self, mem: List[int], a1):
        # print("output" , a1)
        self.output = a1

    def nz(self, mem: List[int], a1, a2):
        if a1 != 0:
            return a2

    def ez(self, mem: List[int], a1, a2):
        if a1 == 0:
            return a2

    def lt(self, mem: List[int], a1, a2, a3):
        mem[a3] = 1 if a1 < a2 else 0

    # def gt(mem: List[int], a1, a2, a3):
    #    mem[a3] = 1 if a1 > a2 else 0

    def eq(self, mem: List[int], a1, a2, a3):
        mem[a3] = 1 if a1 == a2 else 0

    def ex(self, mem: List[int]):
        return len(mem)  # go to end of memory, stops loop.

    opcodes = {
        1: [add, [0, 0, 1]],
        2: [mul, [0, 0, 1]],
        3: [inp, [1]],
        4: [out, [0]],
        5: [nz, [0, 0]],
        6: [ez, [0, 0]],
        7: [lt, [0, 0, 1]],
        8: [eq, [0, 0, 1]],
        99: [ex, []],
    }

    def run(self) -> int:
        mem = self.mem
        i = 0
        while i < len(mem):
            op = mem[i] % 100
            method = self.opcodes[op][0]
            mem_params = self.opcodes[op][1]
            num_params = len(mem_params)
            params = mem[i + 1: i + 1 + num_params]

            inst = str(mem[i])
            modes_list = [int(x) for x in list(inst.zfill(num_params + 2)[:-2])]
            modes_list.reverse()
            for u in range(0, len(modes_list)):
                if modes_list[u] == 0 and mem_params[u] != 1:
                    params[u] = mem[params[u]]

            new_pos = method(self, mem, *params)
            if isinstance(new_pos, int):
                i = new_pos
            else:
                i += num_params + 1
        return self.output


def test_permutation(perm: Tuple, mem: str, max_signal: int, res: Tuple):
    signal = 0
    for elem in perm:
        signal = Machine([signal, elem], mem).run()

    if signal > max_signal:
        max_signal = signal
        res = perm
    return max_signal, res


def main(lines: List[str]):
    mem = lines[0]
    max_signal = 0
    res = ()

    # max_signal, res = test_permutation((4, 3, 2, 1, 0), mem, max_signal, res)
    # print(max_signal, res)
    # exit()

    for perm in list(permutations(range(0, 5))):
        max_signal, res = test_permutation(perm, mem, max_signal, res)

    print(*res, " max  signal: ", max_signal, sep='')


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
