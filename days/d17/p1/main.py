#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List, NamedTuple
import turtle

from intcode import Machine


class Event(NamedTuple):
    num: int
    ev: str


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)


class MazeGame:
    gsx: int
    gsy: int

    mac: Machine
    map: List[int]
    droid_pos: Point
    oxy_pos: Point

    keys: List[str]
    directions: List[Point]
    screen: turtle.Screen
    canvas: turtle.ScrolledCanvas
    display_mul: int
    operating: bool

    intersections: List[Point]
    backtrack: List[int]
    solutions: List[int]

    def getPoint(self, p: Point) -> int:
        if p.x < 0 or p.y < 0 or p.x >= self.gsx or p.y >= self.gsy:
            return ord('.')
        return self.map[p.y * self.gsx + p.x]

    def __init__(self, m: Machine):
        self.mac = m
        out = self.mac.run()
        self.gsx = out.index(ord("\n"))
        self.gsy = int(len(out) / self.gsx)
        self.map = [i for i in out if i != ord('\n')]

        ind_droid = self.map.index(ord('^'))
        self.droid_pos = Point(ind_droid % self.gsx, int(ind_droid / self.gsx))

        self.keys = ["Down", "Up", "Left", "Right"]
        self.directions = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]

        self.operating = False
        self.backtrack = [1, 0, 3, 2]
        self.solutions = []
        self.intersections = []
        self.max_iter = 0

    def set_turtle_pos(self, pos: Point):
        turtle.setpos((pos.x - self.gsx / 2) * self.display_mul,
                      (pos.y - self.gsy / 2) * self.display_mul)

    def draw_rectangle(self, pos: Point, col, ratio: int):
        bx = pos.x - self.gsx / 2
        by = -pos.y + self.gsx / 2
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

    def get_intersections(self):
        for y in range(0, self.gsy):
            for x in range(0, self.gsx):
                curr = Point(x,y)
                if self.getPoint(curr) == ord("."):
                    continue
                is_inter = True
                for elem in self.directions:
                    if self.getPoint(curr + elem) == ord("."):
                        is_inter = False
                if is_inter:
                    self.intersections.append(curr)
        print(self.intersections)


def main(lines: List[str]):
    m = Machine([], lines[0])

    #out = m.run()
    #for elem in out:
    #    print(chr(elem), end="")
    #exit()

    maze = MazeGame(m)
    maze.get_intersections()

    s = 0
    for elem in maze.intersections:
        s += elem.x * elem.y
    print(s)
    exit()
    # maze.play_maze_manual()
    # turtle.tracer(0, 0)

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
