#!/usr/bin/env python3

from __future__ import annotations

import sys
import copy
import time
import curses
from dataclasses import dataclass
from itertools import permutations
from typing import List, Dict, Tuple, Sequence, NamedTuple, TextIO
from inspect import signature
import collections


@dataclass
class Component:
    element: Transaction
    quantity: int


@dataclass
class Transaction:
    name: str
    min_generated: int
    components: List[Component]

    remain: int = 0
    total_generated: int = 0

    def generate(self, quantity: int):
        quantity -= self.remain
        self.remain = 0
        if quantity <= 0:
            self.remain -= quantity
            return

        ratio = round((quantity / self.min_generated) + 0.4999999)

        op_remain = ratio * self.min_generated - quantity
        self.remain += op_remain
        self.total_generated += quantity + op_remain

        #print("generated ", quantity + op_remain, self.name)



        for comp in self.components:
            comp.element.generate(comp.quantity * ratio)

    def reset(self):
        self.remain = 0
        self.total_generated = 0

def generate_transaction_list(lines: List[str]) -> List[Transaction]:
    transactions = [Transaction("ORE", 1, [])]
    for line in lines:
        comps, t = line.split("=>")
        gen, name = t.strip().split(' ')

        trans = next((x for x in transactions if x.name == name), None)
        if trans is None:
            trans = Transaction(name, int(gen), [])
            transactions.append(trans)
        else:
            trans.min_generated = int(gen)

        for c in comps.split(","):
            gen, name = c.strip().split(' ')

            comp_trans = next((x for x in transactions if x.name == name), None)
            assert (comp_trans != trans)
            if comp_trans is None:
                comp_trans = Transaction(name, -1, [])
                transactions.append(comp_trans)

            component = Component(comp_trans, int(gen))
            trans.components.append(component)
    return transactions


def main(lines: List[str]):
    ore_available = 1000000000000

    transactions = generate_transaction_list(lines)
    fuel = next((x for x in transactions if x.name == "FUEL"), None)
    ore = next((x for x in transactions if x.name == "ORE"), None)

    f_quant = 6000000
    divider = int(f_quant / 2)
    while divider != 1:
        fuel.generate(f_quant)
        ratio = -1 if ore.total_generated >= ore_available else 1
        f_quant += ratio * divider

        divider = int(divider / 2)
        for elem in transactions:
            elem.reset()

    f_quant -= divider
    while True:
        fuel.generate(f_quant)
        if ore.total_generated >= ore_available:
            print("result:", f_quant - 1)
            exit()
        f_quant += 1
        for elem in transactions:
            elem.reset()


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
