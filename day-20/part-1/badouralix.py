from tool.runners.python import SubmissionPy

from collections import defaultdict
from math import prod

import networkx as nx


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Set of corner tiles
        corners = set()
        # Graph of connections between tiles with at least one matching border
        grid = nx.Graph()
        # Useful cache to remember known borders and the associated tiles
        lookup = defaultdict(list)

        for data in s.split("\n\n"):
            node = int(data.split("\n")[0][5:-1])
            tile = tuple(tuple(line) for line in data.split("\n")[1:])

            grid.add_node(node)

            # Hopefully the input is already stripped and there is no lingering empty line
            borders = [
                tile[0],
                tile[-1],
                tuple(line[0] for line in tile),
                tuple(line[-1] for line in tile),
            ]

            # For each border, we try to find a matching border in previously seen tiles
            # In the end, adjacent tiles will be neighbors in the grid
            # But here all borders can be reversed independently
            # So potentially we can also match tiles that would not have matched if we had respected some orientation constraint
            for border in borders:
                if border[::-1] in lookup:
                    border = border[::-1]
                for neighbor in lookup[border]:
                    grid.add_edge(node, neighbor)
                lookup[border].append(node)
            pass

        # Assume that we can find corner tiles by looking at the number of neighbors in our graph
        # This might be wrong since our heuristic is garbage
        for node in grid.nodes():
            if len(list(grid.neighbors(node))) == 2:
                corners.add(node)

        return prod(corners)


def test_badouralix():
    assert (
        BadouralixSubmission().run(
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
