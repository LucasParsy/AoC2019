#!/usr/bin/env python3

from __future__ import annotations

from turtle import Screen, RawTurtle, Canvas, TurtleScreen
import tkinter as tk
from dataclasses import dataclass
import turtle
from random import shuffle, seed
from time import sleep
from typing import Dict, List, NamedTuple, Tuple
from Point import Point

@dataclass
class ClignoElem():
    color: str
    pos: Point
    numClign: int
    visible: bool

@dataclass
class Turtle_mode():
    turtle: turtle.Turtle
    screen: Screen
    canvas: Canvas
    speed: int
    gsx: int
    gsy: int
    dimensions: Point
    rotations: Dict(Point, int)
    keys: List[str]
    colors: List[str]
    elemsPos: List[List(Point, Point)]
    bgColor : str
    display_mul: int

    def __init__(self, gsx, gsy, numKeys: int) -> None:
        self.gsx = gsx
        self.gsy = gsy
        self.speed = 1
        self.center = Point(self.gsx // 2, self.gsy // 2)
        self.dimensions = Point(1900,1000)
        self.elemsPos = []
        for _ in range(numKeys):
            self.elemsPos.append([None, None, None]) 
        self._turtle_init()

    def _turtle_init(self):
        self.bgColor = "#010026"
        self.display_mul = 12
        self.turtleSize = 0.75
        self.rotations = {Point(0,1): -90, Point(0,-1): 90, Point(1,0): 0, Point(-1,0): 180}
        self.keys = ["Down", "Up", "Left", "Right"]
        self.colors = ["#be4a2f", "#d77643", "#ead4aa",
                       "#e4a672", "#b86f50",    "#733e39",    "#a22633",
                       "#e43b44", "#f77622",    "#feae34",    "#fee761",    "#63c74d",
                       "#3e8948", "#265c42",    "#193c3e",    "#124e89",    "#0099db",    "#2ce8f5",
                       "#c0cbdc", "#8b9bb4",    "#5a6988",    "#3a4466",    "#ff0044",
                       "#68386c",  "#b55088", "#f6757a",    "#e8b796", "#c28569"
                       ]
        seed(10)
        shuffle(self.colors)

        root = tk.Tk()
        photo = tk.PhotoImage(file = "./santa_bot.gif")
        root.iconphoto(False, photo)
        root.title("cocaino-rap tortue")
        root.geometry("+0+0")
        canvas = tk.Canvas(root, width=self.dimensions.x, height=self.dimensions.y,
                            highlightthickness=0, borderwidth=0)
        canvas.pack()
        self.screen = TurtleScreen(canvas)
        self.canvas = canvas
        self.turtle = RawTurtle(self.canvas)

        #self.screen.setup(self.dimensions.x, self.dimensions.y, 0, 0)
        #self.screen.title("cocaino-rap tortue")
        self.turtle.shapesize(self.turtleSize)
        self.turtle.screen.bgpic("z_bg_nebula16.gif")
        self.turtle.shape("turtle")
        self.turtle.color("red")
        self.turtle.speed(self.speed)
        self.turtle.pensize(2)
        self.turtle.penup()

    def _set_turtle_pos(self, pos: Point):
        pos -= self.center
        self.turtle.setpos(pos.x * self.display_mul,
                           pos.y * self.display_mul)

    def _draw_rectangle(self, pos: Point, col, ratio: float):
        pos -= self.center
        bx = pos.x
        by = -pos.y
        self.canvas.create_rectangle((bx - ratio) * self.display_mul, (by - ratio) * self.display_mul,
                                     (bx + ratio) * self.display_mul, (by + ratio) * self.display_mul, fill=col, width=0)

    def _draw_map(self, map: List[str]):
        for y in range(self.gsy):
            for x in range(0, self.gsx):
                pos = Point(x, self.gsy-y)
                c = map[x + (self.gsx * y)]
                if c == '#':                                                                                                                                                                                                                                                                                                                                                                                            
                    self._draw_rectangle(pos, "white", 0.5)                    
                elif ord(c) in range(ord('a'), ord('z')+1):
                    self._draw_rectangle(pos, self.bgColor, 0.5)
                    self._draw_rectangle(pos, self.colors[ord(c) - ord('a')], 0.25)
                    index = ord(c) - ord('a')
                    self.elemsPos[index][0] = pos
                    self.elemsPos[index][2] = index
                elif ord(c) in range(ord('A'), ord('Z')+1):
                    self._draw_rectangle(pos, self.colors[ord(c) - ord('A')], 0.5)
                    index = ord(c) - ord('A')
                    self.elemsPos[index][1] = pos
                else:
                    self._draw_rectangle(pos, self.bgColor, 0.5)

    def clignote(self, clignotations: List[ClignoElem]):
        for cli in clignotations:
            cli.numClign -= 1
            if cli.numClign % 16 == 0:
                cli.visible = not cli.visible
            if cli.numClign == 0:
                clignotations.remove(cli)
                cli.visible = False
            col = cli.color if cli.visible else self.bgColor  
            self._draw_rectangle(cli.pos, col, 0.5)


    def draw_path(self, path: List[Point], pos: Point):
        self.turtle.pendown()
        clignotations : List[ClignoElem] = []
        prevPoint = path[0]
        for elem in path:

            if elem != prevPoint:
                prevPoint = elem
                #self.turtle.speed("slowest")
                #self.turtle.setheading(self.rotations[prevPoint])
                self.turtle.speed(self.speed)
                self._set_turtle_pos(pos)


            self.clignote(clignotations)
            #elem.y = -elem.y
            pos.x += elem.x
            pos.y -= elem.y
            keyCase = [x for x in self.elemsPos if x[0] == pos]
            if keyCase:
                keyCase = keyCase[0]
                self.elemsPos.remove(keyCase)
                self.turtle.pencolor(self.colors[keyCase[2]])
                self._draw_rectangle(pos, self.bgColor, 0.25)
                if keyCase[1]:
                    cliEl = ClignoElem(self.colors[keyCase[2]],
                            keyCase[1], 200, True)
                    clignotations.append(cliEl)
                    self._draw_rectangle(keyCase[1], self.bgColor, 0.5)
            #self._draw_rectangle(pos + Point(0, -7), col, 0.5)

        self.turtle.setheading(self.rotations[prevPoint])
        self._set_turtle_pos(pos)
        while clignotations:
            self.clignote(clignotations)


    def adjustSpeed(self, val: int):
        nVal = self.speed + val
        if  nVal > 9 or nVal < 1:
            return
        self.speed = nVal


    def play_maze_manual(self, map: List[str], path: List[Point], startPoint: Point):
        startPoint.y = self.gsy - startPoint.y
        self._draw_map(map)
        self._set_turtle_pos(startPoint)

        self.screen.onkey(lambda self=self: self.adjustSpeed(-1), "Left")
        self.screen.onkey(lambda self=self: self.adjustSpeed(1), "Right")
        self.screen.listen()
        self.draw_path(path, startPoint)
        # for i in range(0, len(self.keys)):
        #self.screen.onkey(lambda i=i: self.move(i), self.keys[i])
        self.screen.mainloop()
