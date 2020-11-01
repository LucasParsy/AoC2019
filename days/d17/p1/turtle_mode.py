#!/usr/bin/env python3

from __future__ import annotations

from turtle import Screen, RawTurtle, Canvas
from dataclasses import dataclass
import turtle
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
        self.turtle_init()

    def turtle_init(self):
        self.screen = Screen()
        self.canvas = self.screen._canvas
        self.turtle = RawTurtle(self.canvas)
        self.keys = ["Down", "Up", "Left", "Right"]
        
        self.screen.setup(1900, 1000, 0, 0)
        self.display_mul = 20
        self.screen.bgcolor("#010026")
        self.turtle.hideturtle()
        self.santa_icon = "./santa_bot.gif"
        self.turtle.screen.addshape(self.santa_icon)
        self.turtle.shape(self.santa_icon)
        self.turtle.speed("fast")


    def set_turtle_pos(self, pos: Point):
        self.turtle.setpos((pos.x - self.gsx / 2) * self.display_mul,
                      (pos.y - self.gsy / 2) * self.display_mul)
    
    def draw_rectangle(self, pos: Point, col, ratio: float):
        bx = pos.x - self.gsx / 2
        by = -pos.y + self.gsx / 2
        self.canvas.create_rectangle((bx - ratio) * self.display_mul, (by - ratio) * self.display_mul,
                                     (bx + ratio) * self.display_mul, (by + ratio) * self.display_mul, fill=col)


    def draw_vertical_limit(self, y: int):
        for x in range(self.gsx+2):
             self.draw_rectangle(Point(x, y), "darkblue", 0.5)
 
    def draw_map(self, map: List[int]):
        self.draw_vertical_limit(0)
        for y in range(self.gsy):
            self.draw_rectangle(Point(0, y+1), "darkblue", 0.5)
            for x in range(0, self.gsx):
                if map[x + (self.gsx * y)] == ord('#'):
                    self.draw_rectangle(Point(x+1, self.gsy-y), "white", 0.5)                    
            self.draw_rectangle(Point(self.gsx+1, y+1), "darkblue", 0.5)
        self.draw_vertical_limit(self.gsy+1)

        ind = map.index(ord("^"))
        self.set_turtle_pos(Point(ind % self.gsx + 1, self.gsy - (ind // self.gsy) - 2))
        self.turtle.stamp()
        #self.turtle.stamp()

    def play_maze_manual(self, map: List[int]):
        # self.turtle.tracer(0, 0)
        self.draw_map(map)
        #for i in range(0, len(self.keys)):
        #    self.screen.onkey(lambda i=i: self.move(i), self.keys[i])
        self.screen.listen()
        self.screen.mainloop()

