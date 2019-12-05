#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
from inspect import signature
import collections


class Event(NamedTuple):
    num: int
    ev: str


def add(mem: List[int], a1, a2, pos):
    mem[pos] = a1 + a2


def mul(mem: List[int], a1, a2, pos):
    mem[pos] = a1 * a2


def inp(mem: List[int], a1):
    val = 1
    # val = int(input())
    mem[a1] = val


def out(mem: List[int], a1):
    print(mem[a1])


def ex(_: List[int]):
    print("end program")
    # print("mem[0]:", mem[0])
    exit()


opcodes = {
    1: {"meth": add, "mem_params": [0, 0, 1]},
    2: {"meth": mul, "mem_params": [0, 0, 1]},
    3: {"meth": inp, "mem_params": [1]},
    4: {"meth": out, "mem_params": [1]},
    99: {"meth": ex, "mem_params": []},
}


def machine(lines):
    mem = [int(x) for x in lines[0].split(',')]
    i = 0
    while i < len(mem):
        op = mem[i] % 100
        method = opcodes[op].get("meth")
        mem_params = opcodes[op].get("mem_params")
        num_params = len(mem_params)
        params = mem[i + 1: i + 1 + num_params]

        inst = str(mem[i])
        modes_list = [int(x) for x in list(inst.zfill(num_params + 2)[:-2])]
        modes_list.reverse()
        for u in range(0, len(modes_list)):
            if modes_list[u] == 0 and mem_params[u] != 1:
                params[u] = mem[params[u]]

        method(mem, *params)
        i += num_params + 1


def main(lines: List[str]):
    machine(lines)

    # for noun in range(0, 100):
    #     for verb in range(0, 100):
    #         if machine(lines, noun, verb) == expected_out:
    #             print(100 * noun + verb)
    #             exit()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
