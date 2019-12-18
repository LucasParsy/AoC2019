#!/usr/bin/env python3

import sys
import copy
import time
import curses
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple, TextIO
from inspect import signature
import collections


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


gridsize_x = 45
gridsize_y = 24


def init_window(window):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    window.keypad(True)
    window.nodelay(1)


def display_game(window, grid: List[List[int]]):
    pads_cols = [259, 268, 269, 454]
    pads_cols_len = len(pads_cols)
    WHITE = 256
    GREY = 264
    space = ord(" ")
    color = 0

    for y in range(0, gridsize_y):
        for x in range(0, gridsize_x):
            elem = grid[y][x]
            if elem == 0:
                color = 0
            if elem == 1:
                color = GREY
            if elem >= 3:
                color = WHITE
            if elem == 2:
                pos = (y * gridsize_y + x) % pads_cols_len
                color = pads_cols[pos]

            window.addch(y, x, space, curses.color_pair(color))
            # print(grid[y][x], end=' ')
        # print()
    window.refresh()


def display_score(window, score):
    window.addstr(int(gridsize_y / 2) + 1, gridsize_x + 8, str(score).zfill(8), curses.color_pair(512))


def display_game_over(window):
    window.addstr(gridsize_y - 5, int(gridsize_x / 2), "GAME OVER", curses.color_pair(258))


def display_input(window, inp):
    aff = str(inp)
    if inp == 1:
        aff = "->"
    if inp == -1:
        aff = "<-"
    window.addstr(int(gridsize_y / 2) + 4, gridsize_x + 8, "current input: " + aff)


def save_game(grid: List[List[int]], mac: Mach2, score: int):
    return {
        "score": score,
        "mac": copy.deepcopy(mac),
        "grid": copy.deepcopy(grid)
    }


def get_input(window) -> int:
    c = 0
    try:
        c = window.getkey()
        while True:
            window.getkey()
    except:
        pass
    inp = 0
    if c == "KEY_LEFT":
        inp = -1
    if c == "KEY_RIGHT":
        inp = 1
    return inp


def playgame(window, grid: List[List[int]], mac: Mach2, ball_pos, raq_pos: int):
    score = 0

    is_going_down = True
    save = save_game(grid, mac, score)

    init_window(window)
    window.addstr(int(gridsize_y / 2), gridsize_x + 8, "Score:")
    display_score(window, score)
    display_game(window, grid)

    while not mac.ended():
        time.sleep(0.0001)
        # inp = get_innput(window)
        diff = ball_pos[0] - raq_pos
        if diff < 0:
            inp = -1
        elif diff > 0:
            inp = 1
        else:
            inp = 0
        raq_pos += inp
        display_input(window, inp)
        mac.add_input(inp)
        diff = mac.run()
        for i in range(0, len(diff), 3):
            x, y, v = diff[i: i + 3]
            if x == -1 and y == 0:
                score = v
                display_score(window, score)
            else:
                grid[y][x] = v
            if v == 4:
                ball_pos = (x, y)

        if grid[gridsize_y - 2].count(4):
            if not is_going_down:
                save = save_game(grid, mac, score)
            is_going_down = not is_going_down
        if grid[gridsize_y - 1].count(4):
            time.sleep(100)
            score = save["score"]
            mac = copy.deepcopy(save["mac"])
            grid = copy.deepcopy(save["grid"])
            is_going_down = True
            display_score(window, score)
            # display_game_over(window)
            # window.refresh()
            # exit()

        display_game(window, grid)
    time.sleep(100)

def main(lines: List[str]):
    print("getting breakout game")
    m = Mach2([], "2" + lines[0][1:])
    inp = m.run()

    # print(inp)
    grid = []
    for i in range(0, gridsize_y):
        grid.append([0] * gridsize_x)

    ball_pos = (0, 0)
    raq_pos = 0
    for i in range(0, len(inp), 3):
        if inp[i + 2] == 4:
            ball_pos = (inp[i], inp[i + 1])
        if inp[i + 2] == 3:
            raq_pos = inp[i]
        grid[inp[i + 1]][inp[i]] = inp[i + 2]

    curses.wrapper(playgame, grid, m, ball_pos, raq_pos)


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
