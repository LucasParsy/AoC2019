#!/usr/bin/env python3

import sys
from typing import List, NamedTuple


class Event(NamedTuple):
    num: int
    ev: str


def main(lines: List[str]):
    width = 25
    height = 6
    image_size = width * height
    line_num = [int(x) for x in list(lines[0])]
    layers = [line_num[x:x + image_size] for x in range(0, len(line_num), image_size)]
    image_nums = [[x[pos] for x in layers if x[pos] != 2][0] for pos in range(0, image_size)]
    final_image = [" " if x == 0 else "\u25A0" for x in image_nums]

    for x in range(0, image_size, width):
        print(*final_image[x: x + width], sep=" ")


def print_input(lines: List[str]):
    print("-----BEGIN INPUT-----", file=sys.stderr)
    print(lines, file=sys.stderr)
    print("-----END INPUT-----\n", file=sys.stderr)


if __name__ == "__main__":
    with open("input.txt", "r") as infile:
        inputLines = [line.rstrip("\n") for line in infile.readlines()]
    # print_input(inputLines)
    main(inputLines)
