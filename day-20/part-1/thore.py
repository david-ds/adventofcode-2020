from collections import defaultdict
from math import prod

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        matched_sides = defaultdict(int)
        border_index = {}
        for piece_str in s.split("\n\n"):
            piece_lines = piece_str.splitlines()
            pid = int(piece_lines[0].split(" ")[1][:-1])
            piece = [[c == "#" for c in line] for line in piece_lines[1:]]

            for border in [
                tuple(row[0] for row in piece),
                tuple(piece[0]),
                tuple(row[-1] for row in piece),
                tuple(piece[-1]),
            ]:
                if border in border_index:
                    matched_sides[pid] += 1
                    other_pid = border_index[border]
                    matched_sides[other_pid] += 1
                elif border[::-1] in border_index:
                    matched_sides[pid] += 1
                    other_pid = border_index[border[::-1]]
                    matched_sides[other_pid] += 1
                border_index[border] = pid

        # We assume that two sides don't match if they shouldn't be stitched together
        corners = [p for p, ms in matched_sides.items() if ms == 2]
        return prod(corners)


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
