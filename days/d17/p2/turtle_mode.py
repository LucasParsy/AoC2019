#!/usr/bin/env python3

from __future__ import annotations

from turtle import Screen, RawTurtle, Canvas
from dataclasses import dataclass
import turtle
from time import sleep
from typing import List, NamedTuple

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

@dataclass
class Turtle_mode():
    turtle: Turtle
    screen: Screen
    canvas: Canvas
    gsx: int
    gsy: int
    keys: List[str]
    display_mul: int
 

    def __init__(self, gsx, gsy) -> None:
        self.gsx = gsx
        self.gsy = gsy
        self._turtle_init()

    def _turtle_init(self):
        self.screen = Screen()
        self.canvas = self.screen._canvas
        self.turtle = RawTurtle(self.canvas)
        self.keys = ["Down", "Up", "Left", "Right"]
        
        self.screen.setup(1900, 1000, 0, 0)
        self.display_mul = 20
        self.screen.bgcolor("#010026")
        #self.turtle.hideturtle()
        self.santa_icon = "./santa_bot.gif"
        #self.turtle.screen.addshape(self.santa_icon)
        self.turtle.shape("arrow")
        self.turtle.color("red")
        #self.turtle.shape(self.santa_icon)
        self.turtle.speed("slowest")
        self.turtle.penup()
        self.turtle.hideturtle()


    def _set_turtle_pos(self, pos: Point):
        self.turtle.setpos((pos.x - self.gsx / 2) * self.display_mul,
                      (pos.y - self.gsy / 2) * self.display_mul)
    
    def _draw_rectangle(self, pos: Point, col, ratio: float):
        bx = pos.x - self.gsx / 2
        by = -pos.y + self.gsx / 2
        self.canvas.create_rectangle((bx - ratio) * self.display_mul, (by - ratio) * self.display_mul,
                                     (bx + ratio) * self.display_mul, (by + ratio) * self.display_mul, fill=col)


    def _draw_vertical_limit(self, y: int):
        for x in range(self.gsx+2):
             self._draw_rectangle(Point(x, y), "darkblue", 0.5)
 
    def _draw_map(self, map: List[int]) -> Point :
        self._draw_vertical_limit(0)
        for y in range(self.gsy):
            self._draw_rectangle(Point(0, y+1), "darkblue", 0.5)
            for x in range(0, self.gsx):
                if map[x + (self.gsx * y)] == ord('#'):
                    self._draw_rectangle(Point(x+1, self.gsy-y), "white", 0.5)                    
            self._draw_rectangle(Point(self.gsx+1, y+1), "darkblue", 0.5)
        self._draw_vertical_limit(self.gsy+1)

        ind = map.index(ord("^"))

        startPoint = Point(ind % self.gsx + 1, self.gsy - (ind // self.gsy) - 2)
        self._set_turtle_pos(startPoint)
        self.turtle.setheading(90)
        #self.turtle.stamp()
        return startPoint
        #self.turtle.stamp()

    def draw_path(self, path: str, patterns: List[List[str]], pos: Point):
        directions = [Point(1, 0), Point(0, 1),
                           Point(-1, 0), Point(0, -1)]

        colors = ["#00E322", "#FF8400", "#9700A4"]
        for letter in patterns[0].split(","):
            index = ord(letter) - ord('A')
            col = colors[index]
            patt = patterns[index+1]

            for instru in patt.split(","):
                rot = self.turtle.heading()
                dirIndex = directions[int(rot // 90)]
                if instru == "L": self.turtle.setheading(rot + 90)
                elif instru == "R": self.turtle.setheading(rot - 90) 
                else:
                    for _ in range(int(instru)):
                        pos += dirIndex
                        self._draw_rectangle(pos + Point(0, 4), col, 0.5)
                        self._set_turtle_pos(pos)
                        self.turtle.showturtle()
                        #self.turtle.stamp()
                        #sleep(1)




    def play_maze_manual(self, map: List[int], path: str, patterns: List[List[str]]):
        # self.turtle.tracer(0, 0)
        start = self._draw_map(map)
        self.draw_path(path, patterns, start)
        #for i in range(0, len(self.keys)):
        #    self.screen.onkey(lambda i=i: self.move(i), self.keys[i])
        self.screen.listen()
        self.screen.mainloop()

