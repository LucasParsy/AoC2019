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
        self.output = None
        self.ended = False

        self._input = inp
        self._mem = [int(x) for x in mem_str.split(',')]
        self._counter = 0

    def add_input(self, inp: int):
        self._input.append(inp)

    def _add(self, mem: List[int], a1, a2, pos):
        mem[pos] = a1 + a2

    def _mul(self, mem: List[int], a1, a2, pos):
        mem[pos] = a1 * a2

    def _inp(self, mem: List[int], a1):
        # val = int(input())
        val = self._input.pop(0)
        mem[a1] = val

    def _out(self, mem: List[int], a1):
        # print("output" , a1)
        self.output = a1

    def _nz(self, mem: List[int], a1, a2):
        if a1 != 0:
            return a2

    def _ez(self, mem: List[int], a1, a2):
        if a1 == 0:
            return a2

    def _lt(self, mem: List[int], a1, a2, a3):
        mem[a3] = 1 if a1 < a2 else 0

    # def gt(mem: List[int], a1, a2, a3):
    #    mem[a3] = 1 if a1 > a2 else 0

    def _eq(self, mem: List[int], a1, a2, a3):
        mem[a3] = 1 if a1 == a2 else 0

    def _ex(self, mem: List[int]):
        return len(mem)  # go to end of memory, stops loop.

    _opcodes = {
        1: [_add, [0, 0, 1]],
        2: [_mul, [0, 0, 1]],
        3: [_inp, [1]],
        4: [_out, [0]],
        5: [_nz, [0, 0]],
        6: [_ez, [0, 0]],
        7: [_lt, [0, 0, 1]],
        8: [_eq, [0, 0, 1]],
        99: [_ex, []],
    }

    def run(self) -> int:
        mem = self._mem
        while self._counter < len(mem):
            if self.output is not None:
                out = self.output
                self.output = None
                return out

            op = mem[self._counter] % 100
            method = self._opcodes[op][0]
            mem_params = self._opcodes[op][1]
            num_params = len(mem_params)
            params = mem[self._counter + 1: self._counter + 1 + num_params]

            inst = str(mem[self._counter])
            modes_list = [int(x) for x in list(inst.zfill(num_params + 2)[:-2])]
            modes_list.reverse()
            for u in range(0, len(modes_list)):
                if modes_list[u] == 0 and mem_params[u] != 1:
                    params[u] = mem[params[u]]

            new_pos = method(self, mem, *params)
            if isinstance(new_pos, int):
                self._counter = new_pos
            else:
                self._counter += num_params + 1

        self.ended = True
        return self.output


def test_permutation(perm: Tuple, mem: str, max_signal: int, res: Tuple):
    signal = 0
    machines = [Machine([elem], mem) for elem in perm]

    i = 0
    len_mach = len(machines)
    signal = 0
    while True:
        machines[i % len_mach].add_input(signal)
        temp_sig = machines[i % len_mach].run()
        if temp_sig is None:
            break
        else:
            signal = temp_sig
            i += 1

    if signal > max_signal:
        max_signal = signal
        res = perm
    return max_signal, res


def main(lines: List[str]):
    mem = lines[0]
    max_signal = 0
    res = ()

    for perm in list(permutations(range(5, 10))):
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
