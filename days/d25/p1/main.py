#!/usr/bin/env python3

from __future__ import annotations
from collections.abc import Set
from itertools import combinations, permutations, count, islice

from prompt_toolkit import output
from moddedPrompt.CustomWordCompleter import WordCompleter

import sys
import pickle
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, List, NamedTuple, Optional, OrderedDict, Tuple, Dict, TypeVar
from copy import copy, deepcopy
from datetime import timedelta, datetime
from glob import glob
import collections
import itertools
import math

from prompt_toolkit import prompt
# my custom modification of prompt toolkit
from moddedPrompt.CustomNestedCompleter import NestedCompleter
from moddedPrompt.base import Completion


from Point import Point
from intcode import Machine


@dataclass
class SaveState:
    inventory: List[str]
    roomObjects: List[str]
    machine: Machine
    outputBuffer: str
    lastInput: str


@dataclass
class Game:
    program: str

    machine: Machine = 0
    currentRoom: str = ""
    outputBuffer: str = ""
    lastInput: str = ""
    inventory: List[str] = field(default_factory=list)
    roomObjects: List[str] = field(default_factory=list)
    visitedRooms: Dict[str: List[str]] = field(default_factory=dict)
    roomsDirections: List[str] = field(default_factory=list)
    states: Deque[SaveState] = field(
        default_factory=lambda: collections.deque([], 5))

    operationsLockCap = 10000

    directions = {'north': Point(0, 1), 'south': Point(0, -1),
                  'east': Point(1, 0), 'west': Point(-1, 0)}
    bannedItems = ["escape pod", "giant electromagnet",
                   "molten lava", "photons", "infinite loop"]

    def __post_init__(self) -> None:
        self.states = collections.deque([], 5)
        self.machine = Machine([], self.program)
        self.save()

    def save(self) -> bytes:
        s = self
        state = pickle.dumps([s.machine, s.currentRoom, s.outputBuffer[:-1],
                              s.lastInput, s.inventory, s.roomObjects,
                              s.visitedRooms, s.roomsDirections])
        self.states.appendleft(state)
        return state

    def rollback(self, steps: int, state: Optional[bytes] = None):
        if steps >= len(self.states):
            print("not enough states to roll back, sorry")
            return
        if not state:
            state = self.states[steps]
            print(f"rolled back {steps} steps")
        s = self
        s.machine, s.currentRoom, s.outputBuffer, s.lastInput, \
            s.inventory, s.roomObjects, s.visitedRooms, \
            s.roomsDirections = pickle.loads(state)

    def getItemsFromTextList(self, lines: List[str], i: int) -> Tuple(int, List[str]):
        res = []
        i += 1
        while lines[i].startswith("- "):
            res.append(lines[i][lines[i].index(" ")+1:])
            i += 1
        return (i, res)

    def parseLocationDescription(self, text: str):
        if not text.startswith("== "):
            return

        lines = text.split("\n")
        fl = lines[0]
        roomName = fl[3:-3]
        if not roomName in self.visitedRooms:
            self.visitedRooms[roomName] = {}

        if self.lastInput:
            self.visitedRooms[self.currentRoom][self.lastInput] = None
        self.currentRoom = roomName

        i = 0
        directions = []
        items = []
        while i != len(lines):
            if lines[i] == "Doors here lead:":
                i, directions = self.getItemsFromTextList(lines, i)
            if lines[i] == "Items here:":
                i, items = self.getItemsFromTextList(lines, i)
            i += 1
        self.roomObjects = items
        self.roomsDirections = directions

    def parseInventoryText(self, text: str):
        taking = "You take the "
        dropping = "You drop the "
        if text.startswith(taking):
            object = text[len(taking):text.index('.')]
            self.inventory.append(object)
            self.roomObjects.remove(object)
        if text.startswith(dropping):
            object = text[len(dropping):text.index('.')]
            self.inventory.remove(object)
            self.roomObjects.append(object)

    def generateItemPrompt(self, itemList: List[str]) -> Dict[Completion]:
        d2 = {}
        for item in itemList:
            isDangerous = item in self.bannedItems
            color = "ansired" if isDangerous else "ansiblack"
            d2[Completion(item, style=f"fg:{color}")] = None
        return d2

    def generateCustomPrompt(self) -> NestedCompleter:
        d = OrderedDict()
        for direction in self.roomsDirections:
            isVisited = direction in self.visitedRooms[self.currentRoom]
            color = "ansibrightblack" if isVisited else "ansiblack"
            d[Completion(direction, style=f"fg:{color}")] = None

        if self.roomObjects:
            d["take"] = self.generateItemPrompt(self.roomObjects)
        if self.inventory:
            d["drop"] = self.generateItemPrompt(self.inventory)

        d["rollback"] = None
        d["inv"] = None
        completer = NestedCompleter.from_nested_dict(d)
        return completer

    def inputMachine(self, inp: str):
        self.lastInput = inp
        intInp = [ord(c) for c in inp+'\n']
        self.machine._input = intInp
        self.machine._output.clear()

    def stepGame(self) -> Tuple(bool, str):
        s = self
        numOperationsLock = 0
        while True:
            if s.machine._output:
                s.outputBuffer += chr(s.machine._output[0])
                #print(f"{outputBuffer}", end="\n")
                if s.outputBuffer[-8:] == "Command?":
                    s.save()
                    text = s.outputBuffer.lstrip('\n')
                    self.parseLocationDescription(text)
                    self.parseInventoryText(text)
                    out = s.outputBuffer[:-8]
                    s.outputBuffer = ""
                    return (True, out)
                s.machine._output.clear()
            numOperationsLock += 1
            if numOperationsLock == s.operationsLockCap:
                return (False, s.outputBuffer)
            s.machine.step()

        return (True, "")

    def autoplayAllPlaces(self, previousDirection: str = "",
                          stopAtDoor: Optional[bool] = False) -> bool:
        _, out = self.stepGame()
        isSecurityCheckpoint = "== Security Checkpoint ==" in out
        print(out)
        if isSecurityCheckpoint and stopAtDoor:
            return False
        for item in self.roomObjects:
            if item not in self.bannedItems:
                self.inputMachine(f"take {item}")
                _, out = self.stepGame()
                print(out)
        for dir in self.roomsDirections:
            isVisited = dir in self.visitedRooms[self.currentRoom]

            if not isVisited:
                if isSecurityCheckpoint and dir == "south":
                    continue
                self.inputMachine(dir)
                print(">", dir)
                if not self.autoplayAllPlaces(dir, stopAtDoor):
                    if previousDirection == "":
                        self.visitedRooms = {self.currentRoom: {}}
                        self.inputMachine("inv")
                    return False

        if previousDirection != "":
            n = self.directions[previousDirection]
            n = n.reverse()
            reverseDir = list(self.directions.keys())[
                list(self.directions.values()).index(n)]
            self.inputMachine(reverseDir)
            print("> reverse", reverseDir)
            _, out = self.stepGame()
            print(out)
        else:
            self.visitedRooms = {self.currentRoom: {}}
            self.inputMachine("inv")
        return True

    def autoplayPressurePlate(self):
        errorMess = 'A loud, robotic voice says "Alert!'
        save = self.save()
        combs = []
        for i in range(0, len(self.inventory)):
            combs += list(combinations(self.inventory, i))
        print(combs)

        output = ""
        for c in combs:
            for item in c:
                self.inputMachine(f"drop {item}")
                self.stepGame()

            self.inputMachine("south")
            _, output = self.stepGame()
            if errorMess not in output:
                break
            self.rollback(0, save)
        print(output)
        self.inputMachine("inv")

    def play(self):
        s = self
        s.autoplayAllPlaces('', False)
        s.autoplayAllPlaces('', True)
        s.autoplayPressurePlate()
        while True:
            successOutcome, outputStr = s.stepGame()
            if successOutcome:
                print(outputStr)
                inp = prompt("> ", completer=self.generateCustomPrompt())
                if inp.startswith("rollback"):
                    num = 1
                    splitInp = inp.split(' ')
                    if len(splitInp) == 2:
                        num = int(splitInp[1])
                    s.rollback(num)
                    continue
                if inp == "exit":
                    exit()
                self.inputMachine(inp)
            else:
                print(outputStr)
                r = prompt(
                    "you seem stuck on an infinite loop... rollback? [Y/n] ",
                    completer=WordCompleter(["Y", "n"]))
                if r.lower() == "y":
                    s.rollback(1)


def main(lines: List[str]):
    m = Game(lines[0])
    m.play()


def unique_test():
    pass


def fileTest(lines: List[str], expected: str):
    pass
    #assert(res == expected)


def unit_test():
    start = datetime.now()
    unique_test()
    for fname in glob("./tests/*.txt"):
        print("---", fname, "---")
        with open(fname, "r") as f:
            expected = fname.split('-')[1]
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            fileTest(inputLines, expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs")
    # if delta < bestTime:
    #print("new record!")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    # sys.setrecursionlimit(99999)
    unit_test()

    file = "input.txt"
    with open(file, "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
