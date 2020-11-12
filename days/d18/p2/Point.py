#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import List, NamedTuple, Tuple, Dict


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point):
        return Point(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f'Point({self.x},{self.y})'

    def __repr__(self) -> str:
        return self.__str__()
    
    def __hash__(self) -> int:
        return self.x * 10 + self.y

    def reverse(self) -> Point:
        return Point(-self.x, -self.y)
        #self.x = -self.x
        #self.y = -self.y
