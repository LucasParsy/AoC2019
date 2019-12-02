#!/usr/bin/env python3

# *******
# * Read input from STDIN
# * Use: echo or print to output your result to STDOUT, use the /n constant at the end of each result line.
# * Use: sys.stderr.write() to display debugging information to STDERR
# * ***/
import sys
from typing import List, Dict, Tuple, Sequence, NamedTuple
import collections


class Event(NamedTuple):
    num: int
    ev: str

def main():
    pos = [i for i in range(1,21)]
    events = []
    favorite = int(sys.stdin.readline())
    sys.stdin.readline()
    for line in sys.stdin:
        elem = (Event(*line.rstrip('\n').split()))
        if elem.ev == "I":
            pos.remove(int(elem.num))
        else:
            try:
                ind1 = pos.index(int(elem.num))
                ind2 = ind1 - 1
                pos[ind1], pos[ind2] = pos[ind2], pos[ind1]
            except:
                pass

    try:
        print(pos.index(pos.index(favorite)) + 1)
    except:
        print("KO")
    # print(lines)


def print_input():
    print("-----BEGIN INPUT-----", file=sys.stderr)
    for line in sys.stdin:
        print(line.rstrip('\n'), file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    # print_input()
    main()
