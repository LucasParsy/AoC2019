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

resDir = "/run/media/tuxlu/Données/proj/codeExercises/adventOfCode2019/icons/"


@dataclass
class ClignoElem():
    color: str
    pos: Point
    numClign: int
    visible: bool


@dataclass
class Turtle_mode():
    turtles: List[turtle.Turtle]
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
    bgColor: str
    display_mul: int

    def __init__(self, gsx, gsy, numKeys: int, numTurtles: int) -> None:
        self.gsx = gsx
        self.gsy = gsy
        self.speed = 1
        self.numTurtles = numTurtles
        self.center = Point(self.gsx // 2, self.gsy // 2)
        self.dimensions = Point(1900, 1000)
        self.elemsPos = []
        for _ in range(numKeys):
            self.elemsPos.append([None, None, None])
        self._turtle_init()

    def _turtle_init(self):
        self.bgColor = "#010026"
        self.display_mul = 12
        self.turtleSize = 0.75
        self.rotations = {Point(0, 1): -90, Point(0, -1): 90, Point(1, 0): 0, Point(-1, 0): 180}
        self.keys = ["Down", "Up", "Left", "Right"]
        self.turtlesColors = ["red", "#00F51E", "#D200FF", "#E4E200"]
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
        photo = tk.PhotoImage(file=resDir+"santa_bot.gif")
        root.iconphoto(False, photo)
        root.title("cocaino-rap tortue")
        root.geometry("+0+0")
        canvas = tk.Canvas(root, width=self.dimensions.x, height=self.dimensions.y,
                           highlightthickness=0, borderwidth=0)
        canvas.pack()
        self.screen = TurtleScreen(canvas)
        self.canvas = canvas

        self.turtles = []
        for i in range(self.numTurtles):
            turtle = RawTurtle(self.canvas)
            turtle.shapesize(self.turtleSize)
            turtle.screen.bgpic(resDir+"z_bg_nebula16.gif")
            turtle.shape("turtle")
            turtle.color(self.turtlesColors[i])
            turtle.speed(self.speed)
            turtle.pensize(2)
            turtle.penup()
            self.turtles.append(turtle)

    def _set_turtle_pos(self, pos: Point, turtle: turtle.Turtle):
        pos -= self.center
        turtle.setpos(pos.x * self.display_mul,
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
                    self._draw_rectangle(
                        pos, self.colors[ord(c) - ord('a')], 0.25)
                    index = ord(c) - ord('a')
                    self.elemsPos[index][0] = pos
                    self.elemsPos[index][2] = index
                elif ord(c) in range(ord('A'), ord('Z')+1):
                    self._draw_rectangle(
                        pos, self.colors[ord(c) - ord('A')], 0.5)
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

    def draw_path(self, robotsPaths: List[Tuple(int, List[Point])],
                  positions: Point):
        for turtle in self.turtles:
            turtle.pendown()
        clignotations: List[ClignoElem] = []

        prevPoint = [Point(0, 1)] * self.numTurtles

        for robot, path in robotsPaths:
            turtle = self.turtles[robot]
            for elem in path:

                if elem != prevPoint[robot]:
                    turtle.tiltangle(self.rotations[prevPoint[robot]])
                    prevPoint[robot] = elem
                    self._set_turtle_pos(positions[robot], turtle)
                    turtle.speed(self.speed)
                    # turtle.speed(7)
                    # turtle.setheading(self.rotations[elem])

                positions[robot].x += elem.x
                positions[robot].y -= elem.y
                pos = positions[robot]

                self.clignote(clignotations)
                keyCase = [x for x in self.elemsPos if x[0] == pos]
                if keyCase:
                    keyCase = keyCase[0]
                    self.elemsPos.remove(keyCase)
                    turtle.pencolor(self.colors[keyCase[2]])
                    self._draw_rectangle(pos, self.bgColor, 0.25)
                    if keyCase[1]:
                        cliEl = ClignoElem(self.colors[keyCase[2]],
                                           keyCase[1], 200, True)
                        clignotations.append(cliEl)
                        self._draw_rectangle(keyCase[1], self.bgColor, 0.5)
                #self._draw_rectangle(pos + Point(0, -7), col, 0.5)

            turtle.tiltangle(self.rotations[prevPoint[robot]])
            self._set_turtle_pos(positions[robot], turtle)

            # turtle.tiltangle(self.rotations[prevPoint[robot]])
            # turtle.setheading(self.rotations[elem])
            # turtle.speed(self.speed)
            #self._set_turtle_pos(positions[robot], turtle)

        while clignotations:
            self.clignote(clignotations)

    def adjustSpeed(self, val: int):
        nVal = self.speed + val
        if nVal > 9 or nVal < 1:
            return
        self.speed = nVal

    def play_maze_manual(self, map: List[str],
                         path: List[Tuple(int, List[Point])],
                         startPoints: List[Point]):
        self._draw_map(map)

        for ind, start in enumerate(startPoints):
            start.y = self.gsy - start.y
            self._set_turtle_pos(start, self.turtles[ind])

        self.screen.onkey(lambda self=self: self.adjustSpeed(-1), "Left")
        self.screen.onkey(lambda self=self: self.adjustSpeed(1), "Right")
        self.screen.listen()
        self.draw_path(path, startPoints)
        # for i in range(0, len(self.keys)):
        #self.screen.onkey(lambda i=i: self.move(i), self.keys[i])
        self.screen.mainloop()
