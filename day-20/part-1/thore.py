from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import product
from math import prod

import numpy as np

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        pieces = list(map(JigsawPiece.from_string, s.split("\n\n")))

        matched_sides = defaultdict(set)
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                p1, p2 = pieces[i], pieces[j]
                for side1, side2, flipped in product(Side, Side, [False, True]):
                    if np.array_equal(p1.border(side1), p2.border(side2, flipped)):
                        matched_sides[p1.pid].add(side1)
                        matched_sides[p2.pid].add(side2)

        # We assume that two sides don't match if they shouldn't be stitched together
        corners = [p for p, ms in matched_sides.items() if len(ms) == 2]
        return prod(corners)


class Side(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


@dataclass
class JigsawPiece:
    pid: int
    image: np.ndarray

    @classmethod
    def from_string(cls, s):
        lines = s.splitlines()
        pid = int(lines[0].split(" ")[1][:-1])
        image = np.array([[c == "#" for c in line] for line in lines[1:]], dtype=bool)
        return cls(pid, image)

    def border(self, side: Side, flipped: bool = False):
        if side == Side.LEFT:
            border = self.image[:, 0]
        elif side == Side.TOP:
            border = self.image[0]
        elif side == Side.RIGHT:
            border = self.image[:, -1]
        elif side == Side.BOTTOM:
            border = self.image[-1]

        if flipped:
            border = border[::-1]

        return border

    def __str__(self):
        res = []
        res.append(f"Tile {self.pid}:")
        res.extend(["".join(["#" if c else "." for c in line]) for line in self.image])
        return "\n".join(res)


def test_day20_part1():
    assert (
        ThoreSubmission().run(
            """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
        )
        == 20899048083289
    )
