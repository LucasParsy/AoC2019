#!/usr/bin/env python3

from __future__ import annotations
from itertools import combinations, permutations, count, islice

import sys
import pickle
from dataclasses import dataclass
from typing import Any, Callable, List, NamedTuple, Tuple, Dict, TypeVar
from copy import copy, deepcopy
from datetime import timedelta, datetime
from glob import glob
import itertools
import math
from decimal import Decimal
from fractions import Fraction

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(math.sqrt(n)-1)))

#big thanks to this solution:
#https://codeforces.com/blog/entry/72593

class CardDealer:

    def cut(self, cards: List[int], index: int) -> List[int]:
        l1 = cards[index:]
        l2 = cards[:index]
        res = l1 + l2
        #print("cut", index, ":", res)
        return res

    def dealIncrement(self, cards: List[int], increment: int) -> List[int]:
        cardsLen = len(cards)
        nl = [-1] * cardsLen
        incInd = 0
        for i in range(cardsLen):
            nl[incInd% cardsLen] = cards[i]
            incInd += increment
        #print("deal with increment", increment, ":", nl)
        return nl

    def dealStack(self, cards: List[int]):
        cards.reverse()
        #print("deal into new stack:", cards)

    def solveP1(self, lines: List[str], numCards: int, cards: List[int]) -> List[int]:
        #print("-----", cards, "------")
        for instruction in lines:
            words = instruction.split(" ")
            if words[0] == "cut":
                cards = self.cut(cards, int(words[-1]))
            elif words[1] == "with":
                cards = self.dealIncrement(cards, int(words[-1]))
            else:
                self.dealStack(cards)
        return cards

    def getEquation(self, lines: List[str], numCards: int) -> Tuple(int, int):
        # ax + b
        a = 1
        b = 0
        for instruction in lines:
            # cx + d
            c = 1
            d = 0
            words = instruction.split(" ")
            if words[0] == "cut":
                d = -int(words[-1])
            elif words[1] == "with":
                c = int(words[-1])
            else:
                c = -1 # numcards - x - 1
                d = numCards - 1
        
            a = a * c % numCards
            b = ((b * c) + d) % numCards
        return (a, b)

    #basic pow in python already does this...
    def pow_mod(self, x, n, m):
        if n == 0:
            return 1
        t = self.pow_mod(x, n//2, m)
        if (n % 2) == 0:
            return (t * t) % m
        else:
            return (t * t * x) % m


    def reverseIncrement(self, ind: int, increment: int, numCards: int) -> int :
        while (ind % increment) != 0:
            ind += numCards
        return (ind // increment)

    def divideWithModularMult(self, ind: int, increment: int, numCards: int) -> int :
        return (ind * self.pow_mod(increment, numCards - 2, numCards)) % numCards

    def getValInd(self, lines: List[str], numCards: int, searchIndex: int, ind : int = -1) -> int:
        if ind == -1:
            ind = searchIndex
        
        for instruction in reversed(lines):
            #print(instruction)
            words = instruction.split(" ")
            if words[0] == "cut":  #couper le paquet
                cutInd = int(words[-1])
                ind  += cutInd
            elif words[1] == "with": #distribuer avec incrément
                ind = self.reverseIncrement(ind, int(words[-1]), numCards)
            else: #inversion paquet
                ind = numCards - 1 - ind
        return ind % numCards


    def  loopInds(self, lines: List[str], numCards: int, searchIndex: int, numLoops: int) -> int:
        ind  = searchIndex

        pattern = []
        print(ind)
        for i in range(numLoops):
            ind =  self.getValInd(lines, numCards, searchIndex, ind)
            #if is_prime(i):
                #print(i, ind)
            if ind == searchIndex:
                print("huh?:", i)
            pattern.append(ind)
            #print(ind)
        return ind

    def  loopAllArr(self, lines: List[str], numCards: int, numLoops: int) -> int:
        inds = list(range(numCards))
        print(inds)
        for i in range(numLoops):
            for index, value in enumerate(inds):
                inds[index] =  self.getValInd(lines, numCards, index, value)
            print(inds)

    def getNthProgressionElement(self, a: int, b: int, n: int, initial: int, numCards: int) -> int:
        r = Fraction(b, 1-a)
        res = (pow(a, n, numCards) * ((initial - r.limit_denominator(800000000000))) % numCards)  + r % numCards
        return round(res % numCards)

    def getNthProgressionElement2(self, a: int, b: int, n: int, initial: int, numCards: int) -> int:
        res = pow(a, n, numCards) * (initial % numCards) + self.divideWithModularMult(b * (1-pow(a,n, numCards)), (1-a % numCards), numCards)
        return res % numCards

    def getReverseNthProgressionElement2(self, a: int, b: int, n: int, pos: int, numCards: int) -> int:
        addPart = self.divideWithModularMult(b * (1-pow(a,n, numCards)), (1-a % numCards), numCards)
        top = (pos - addPart) % numCards
        res = self.divideWithModularMult(top, pow(a,n,numCards), numCards)
        return res

    def getReverseNthProgressionElement(self, a: int, b: int, n: int, pos: int, numCards: int) -> int:
        r = Decimal(b, 1-a)
        res = (pow(a, n) * r) % numCards
        res2 = (pow(a, n, numCards) * (r% numCards)) % numCards
        #assert(res == res2)
        res = (res + (pos - r) % numCards) % numCards
        res = self.divideWithModularMult(res, pow(a, n), numCards)
        return res


def main(lines: List[str]):
    dealer = CardDealer()
    numCards = 119315717514047
    shuffling = 101741582076661
    #print(numCards-shuffling)
    #shuffling = 10007
    #numCards = 10007
    findIndex = 2020
    #findIndex = 2


    #dealer.loopAllArr(lines, 10, 8)
    #numCards = 10
    #cards = dealer.solveP1(lines, numCards, list(range(0, numCards)))
    #print(cards)
    #found = dealer.loopInds(lines, numCards, findIndex, shuffling)

    #print(found)
    #print()
    a,b = dealer.getEquation(lines, numCards)
    print(f"eq: {a}x + {b}")

    origInd = findIndex
    for i in range(1, 1000):
        origInd = (a * origInd + b) % numCards

        otherInd = dealer.getNthProgressionElement2(a,b, i, findIndex, numCards)
        #otherInd %= numCards
        assert(origInd == otherInd)
        reverseInd = dealer.getReverseNthProgressionElement2(a, b, i, otherInd, numCards)
        assert (reverseInd == findIndex)

    #tehRes = dealer.getNthProgressionElement2(a, b, shuffling, findIndex, numCards)
    tehRes = dealer.getReverseNthProgressionElement2(a, b, shuffling, findIndex, numCards)
    print('the final, long awaited solution is...:', tehRes)

        #print(origInd)
        #dealer.divideWithModularMult((findIndex-b), a, numCards)

    #assert(cards[findIndex] == found)
    return
    inds = []    
    for i in range(100):
        cards = dealer.solveP2(lines, numCards)

        print(cards[findIndex], end ="")
        inds.append(cards[findIndex])
    #res = maze.solveP2(lines)
    print(inds)


def unique_test():
    dealer = CardDealer()
    #test reverse modular dividing
    numCards = 23
    dividers = [3, 7, 9]
    for di in dividers:
        for i in range(di +1):
            assert(dealer.reverseIncrement(i, di, numCards) ==
                     dealer.divideWithModularMult(i, di, numCards))

def fileTest(lines: List[str], expected: str):
    numCards = 10
    cards = list(range(0, numCards))
    dealer = CardDealer()
    swapped = dealer.solveP1(lines, numCards, cards)

    a,b = dealer.getEquation(lines, numCards)

    nSwapped = [0] * numCards
    for i in range(numCards):
        nval = (a * i + b) % numCards
        nSwapped[nval] = i
    assert (swapped == nSwapped)


    nSwapped = []
    for i in range(numCards):
        found = dealer.getValInd(lines, numCards, i)
        nSwapped.append(found)
    
    assert (swapped == nSwapped)
    res = [str(i) for i in swapped]
    res = "".join(res)
    assert(res == expected)


def unit_test():
    start = datetime.now()
    unique_test()
    for fname in glob("./tests/*.txt"):
        print("---",fname, "---")
        with open(fname, "r") as f:
            expected = fname.split('-')[1]
            inputLines = [line.rstrip("\n") for line in f.readlines()]
            fileTest(inputLines, expected)

    end = datetime.now()
    delta = (end-start).total_seconds()

    print("done in ", delta, "secs")
    #if delta < bestTime:
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
