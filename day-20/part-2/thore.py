from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, astuple
from enum import IntEnum
from functools import reduce
from itertools import product
from math import sqrt
from typing import Generator, NamedTuple

import numpy as np

from tool.runners.python import SubmissionPy

SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip(
    "\n"
)


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        puzzle = solve_puzzle(s.strip("\n"))

        sea_monster = np.array(
            [[c == "#" for c in line] for line in SEA_MONSTER.splitlines()], dtype=bool
        )
        for transformation in Transformation.get_all():
            puzzle_transformed = transformation.apply_array(puzzle)
            sea_monster_locations = find_pattern(puzzle_transformed, sea_monster)
            if sea_monster_locations:
                break

        return puzzle.sum() - len(sea_monster_locations) * sea_monster.sum()


def find_pattern(puzzle, pattern):
    n, p = puzzle.shape
    k, l = pattern.shape
    return [
        (i, j)
        for i, j in product(range(n - k + 1), range(p - l + 1))
        if (puzzle[i : i + k, j : j + l] & pattern).sum() == pattern.sum()
    ]


def solve_puzzle(s):
    # parse the puzzle pieces
    pieces_by_id = {}
    for piece_str in s.split("\n\n"):
        piece_lines = piece_str.splitlines()
        pid = int(piece_lines[0].split(" ")[1][:-1])
        piece = np.array(
            [[c == "#" for c in line] for line in piece_lines[1:]], dtype=bool
        )
        pieces_by_id[pid] = piece
    n_pieces = len(pieces_by_id)
    size = int(sqrt(n_pieces))  # assumption: square puzzle
    piece_size = next(iter(pieces_by_id.values())).shape[0]  # assumption: square pieces

    # list all matching borders
    matches = defaultdict(dict)
    border_index = {}
    for pid, piece in pieces_by_id.items():
        for side, border in enumerate(
            [
                tuple(piece[:, 0]),
                tuple(piece[0]),
                tuple(piece[:, -1]),
                tuple(piece[-1]),
            ]
        ):
            if border in border_index:
                other_pid, other_side = border_index[border]
                matches[pid][side] = Match(other_pid, other_side, False)
                matches[other_pid][other_side] = Match(pid, side, False)
            elif border[::-1] in border_index:
                other_pid, other_side = border_index[border[::-1]]
                matches[pid][side] = Match(other_pid, other_side, True)
                matches[other_pid][other_side] = Match(pid, side, True)
            border_index[border] = (pid, side)

    corners = [pid for pid in matches if len(matches[pid]) == 2]

    # check the assumption that there isn't any "extra" match, and some sanity checks
    n_matches = sum(len(d) for d in matches.values())
    assert n_matches == 4 * (size - 1) * size, "Wrong number of matches"
    assert len(corners) == 4, "Wrong number of corner pieces"
    assert len([pid for pid in matches if len(matches[pid]) == 3]) == 4 * (
        size - 2
    ), "Wrong number of side pieces"
    assert (
        len([pid for pid in matches if len(matches[pid]) == 4]) == (size - 2) ** 2
    ), "Wrong number of inner pieces"

    # take a corner, transform it as necessary and put it at the top left
    solution = []
    corner_pid = corners[0]
    solution.append(
        (corner_pid, Transformation.align_top_left_corner(*matches[corner_pid].keys()))
    )

    # put the pieces one by one, from left to right and top to bottom
    for i in range(1, n_pieces):
        if i % size == 0:
            # new row: match the bottom side of the first piece of the previous row
            pid, transformation = solution[i - size]
            original_side, flipped = transformation.get_side_after(Side.BOTTOM)
            matching_side = matches[pid][original_side]
            p, s, f = matching_side
            # rotate/transpose the candidate so that the matched side is at the top
            solution.append((p, Transformation.from_target(s, Side.TOP, flipped ^ f)))
        else:
            # continue the row: match the right side of the previous piece
            pid, transformation = solution[i - 1]
            original_side, flipped = transformation.get_side_after(Side.RIGHT)
            matching_side = matches[pid][original_side]
            p, s, f = matching_side
            # rotate/transpose the candidate so that the matched side is at the left
            solution.append((p, Transformation.from_target(s, Side.LEFT, flipped ^ f)))

    # reconstruct the puzzle by stitching the border
    puzzle = np.zeros(((piece_size - 2) * size,) * 2, dtype=bool)
    for i, (pid, transformation) in enumerate(solution):
        x, y = i // size, i % size  # piece coordinates
        transformed_piece = transformation.apply_array(pieces_by_id[pid])
        puzzle[
            (piece_size - 2) * x : (piece_size - 2) * (x + 1),
            (piece_size - 2) * y : (piece_size - 2) * (y + 1),
        ] = transformed_piece[1:-1, 1:-1]
    return puzzle


class Side(IntEnum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

    def __add__(self, rotation):
        return Side((int(self) + rotation) % 4)

    def __sub__(self, rotation):
        return Side((int(self) - rotation) % 4)


class Match(NamedTuple):
    pid: int
    side: Side
    flipped: bool


@dataclass(frozen=True)
class Transformation:
    # these three transformations can generate all the rotations/flips
    transpose: bool
    fliplr: bool
    flipud: bool

    def apply_array(self, array: np.ndarray) -> np.ndarray:
        """Apply the transformation to an array"""
        functions = (
            f for f, b in zip((np.transpose, np.fliplr, np.flipud), astuple(self)) if b
        )
        return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)(array)

    def get_side_after(self, side: Side) -> Side:
        """Apply the transformation and return the new side which replaced side,
        and if it's flipped"""
        t_side, flipped = side, False
        if self.transpose:
            t_side = t_side + 1 if side % 2 == 0 else t_side - 1
        if self.fliplr:
            if side in [Side.LEFT, Side.RIGHT]:
                t_side += 2
            else:
                flipped = True
        if self.flipud:
            if side in [Side.TOP, Side.BOTTOM]:
                t_side += 2
            else:
                flipped = True
        return t_side, flipped

    @classmethod
    def get_all(cls) -> Generator[Transformation, None, None]:
        """Generate all the possible transformations"""
        for transpose, fliplr, flipud in product((False, True), repeat=3):
            yield cls(transpose, fliplr, flipud)

    @classmethod
    def from_target(
        cls, source_side: Side, target_side: Side, flip: bool
    ) -> Transformation:
        """Return the transformation that replace target_side by source_side,
        the latter being possibly flipped"""
        for transfo in cls.get_all():
            if transfo.get_side_after(target_side) == (source_side, flip):
                return transfo

    @classmethod
    def align_top_left_corner(
        cls, matching_side1: Side, matching_side2: Side
    ) -> Transformation:
        """Return the transformation so that the two matching sides are at the
        bottom and right, meaning that the piece can be put at the top left corner"""
        if {matching_side1, matching_side2} == {Side.RIGHT, Side.BOTTOM}:
            return Transformation(False, False, False)
        elif {matching_side1, matching_side2} == {Side.RIGHT, Side.TOP}:
            return Transformation(False, False, True)
        elif {matching_side1, matching_side2} == {Side.LEFT, Side.TOP}:
            return Transformation(False, True, True)
        elif {matching_side1, matching_side2} == {Side.LEFT, Side.BOTTOM}:
            return Transformation(False, True, False)


def test_transformation():
    a = np.arange(9).reshape((3, 3))
    assert np.array_equal(
        Transformation(True, False, False).apply_array(a), np.transpose(a)
    )
    assert np.array_equal(
        Transformation(False, True, False).apply_array(a), np.fliplr(a)
    )
    assert np.array_equal(
        Transformation(False, False, True).apply_array(a), np.flipud(a)
    )
    assert np.array_equal(
        Transformation(True, False, True).apply_array(a), np.flipud(np.transpose(a))
    )
    assert np.array_equal(
        Transformation(True, True, True).apply_array(a),
        np.flipud(np.fliplr(np.transpose(a))),
    )

    assert Transformation(True, False, False).get_side_after(Side.LEFT) == (
        Side.TOP,
        False,
    )
    assert Transformation(True, False, False).get_side_after(Side.BOTTOM) == (
        Side.RIGHT,
        False,
    )
    assert Transformation(False, True, False).get_side_after(Side.RIGHT) == (
        Side.LEFT,
        False,
    )
    assert Transformation(False, True, False).get_side_after(Side.BOTTOM) == (
        Side.BOTTOM,
        True,
    )
    assert Transformation(False, False, True).get_side_after(Side.RIGHT) == (
        Side.RIGHT,
        True,
    )
    assert Transformation(False, False, True).get_side_after(Side.BOTTOM) == (
        Side.TOP,
        False,
    )
    assert Transformation(True, False, True).get_side_after(Side.RIGHT) == (
        Side.BOTTOM,
        True,
    )
    assert Transformation(True, True, True).get_side_after(Side.LEFT) == (
        Side.BOTTOM,
        True,
    )
    assert Transformation(True, True, True).get_side_after(Side.BOTTOM) == (
        Side.LEFT,
        True,
    )

    assert len(list(Transformation.get_all())) == 8

    assert Transformation.from_target(Side.LEFT, Side.LEFT, False) == Transformation(
        False, False, False
    )
    assert Transformation.from_target(Side.LEFT, Side.LEFT, True) == Transformation(
        False, False, True
    )
    assert Transformation.from_target(Side.TOP, Side.LEFT, False) == Transformation(
        True, False, False
    )
    assert Transformation.from_target(Side.BOTTOM, Side.LEFT, False) == Transformation(
        True, True, False
    )
    assert Transformation.from_target(Side.BOTTOM, Side.LEFT, True) == Transformation(
        True, True, True
    )
    assert Transformation.from_target(Side.LEFT, Side.BOTTOM, True) == Transformation(
        True, True, True
    )
    assert Transformation.from_target(Side.RIGHT, Side.LEFT, False) == Transformation(
        False, True, False
    )
    assert Transformation.from_target(Side.RIGHT, Side.LEFT, True) == Transformation(
        False, True, True
    )


TEST_INPUT = """Tile 2311:
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

TEST_SOLVED = """
.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
""".strip(
    "\n"
)


def np_bool_to_string(array: np.ndarray) -> str:
    return "\n".join("".join("#" if c else "." for c in line) for line in array)


def test_solve_puzzle():
    puzzle = solve_puzzle(TEST_INPUT)
    assert any(
        np_bool_to_string(transformation.apply_array(puzzle)) == TEST_SOLVED
        for transformation in Transformation.get_all()
    )


def test_day20_part2():
    assert ThoreSubmission().run(TEST_INPUT) == 273