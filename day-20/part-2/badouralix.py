from tool.runners.python import SubmissionPy

from collections import defaultdict
from functools import lru_cache
from math import cos, pi, sin, sqrt

import networkx as nx
import numpy as np


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Before each run we need to flush the cache to avoid side effects from previous runs
        self.transform.cache_clear()

        # Mapping of tiles to borders in a very specific and known order
        borders = dict()
        # Set of corner tiles
        corners = set()
        # Graph of connections between tiles with at least one matching border
        grid = nx.Graph()
        # Useful cache to remember known borders and the associated tiles
        lookup = defaultdict(list)
        # Number of pixel per tile
        resolution = 0
        # Number of tiles per edge of the image
        size = 0
        # Records of the content of each tile
        tiles = dict()
        # Set of tiles that already have a position in the image
        used = set()

        for data in s.split("\n\n"):
            node = int(data.split("\n")[0][5:-1])
            tile = tuple(tuple(line) for line in data.split("\n")[1:])

            tiles[node] = tile

            grid.add_node(node)

            # Hopefully the input is already stripped and there is no lingering empty line
            # Order matters a lot when iterating over the borders and when computing the transformation action of the tile
            borders[node] = [
                # Upper border going right
                tile[0],
                # Upper border going left
                tile[0][::-1],
                # Lower border going left
                tile[-1][::-1],
                # Lower border going right
                tile[-1],
                # Left border going down
                tuple(line[0] for line in tile),
                # Right border going down
                tuple(line[-1] for line in tile),
                # Right border going up
                tuple(line[-1] for line in tile)[::-1],
                # Left border going up
                tuple(line[0] for line in tile)[::-1],
            ]

            # For every side of the tile, we try to find a matching side in previously seen tiles
            # Taking every other border works to visit each side of the tile because why not
            # In the end, adjacent tiles will be neighbors in the grid
            # But here all borders can be reversed independently
            # So potentially we can also match tiles that would not have matched if we had respected some orientation constraint
            for border in borders[node][::2]:
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

        # Extract some metadata out of the previous parsing stage
        resolution = len(tile)  # Thank you python for not respecting variable scopes
        size = int(sqrt(len(grid.nodes())))

        # Build placement, i.e. the array of tile ids
        # Pray very very hard for the graph we previously built to be a well-formed grid
        placement = [[0] * size for _ in range(size)]
        # Pick randomly one corner and place it on (0, 0)
        position = (0, 0)
        direction = (0, 1)
        node = min(corners)
        placement[position[0]][position[1]] = node
        used.add(node)
        # Fill placement borders
        while True:
            for node in grid.neighbors(placement[position[0]][position[1]]):
                if len(list(grid.neighbors(node))) != 4 and node not in used:
                    break
            else:
                break
            position = (position[0] + direction[0], position[1] + direction[1])
            placement[position[0]][position[1]] = node
            used.add(node)
            if len(list(grid.neighbors(node))) == 2:
                direction = (direction[1], -direction[0])
            pass
        # Fill placement interior
        for i in range(1, size - 1):
            for j in range(1, size - 1):
                node = (
                    set.intersection(
                        set(grid.neighbors(placement[i - 1][j])),
                        set(grid.neighbors(placement[i][j - 1])),
                    )
                    .difference(used)
                    .pop()
                )
                placement[i][j] = node
                used.add(node)

        # Build image by writing all tiles to their respective position and orientation in the image
        intermediate = [[""] * size * resolution for _ in range(size * resolution)]
        # Write the first tile, by using some black magic to flip it horizontally or vertically if needed
        node = placement[0][0]
        tile = tiles[node]
        # Here we figure out the orientation of the first tile by trying them exhaustively
        for action in range(8):
            rotatedtile = self.transform(tile, action)
            # The lower border must match the tile below and the right border the tile on the right-hand side
            if (rotatedtile[-1] in borders[placement[1][0]]) and (
                tuple(line[-1] for line in rotatedtile) in borders[placement[0][1]]
            ):
                break
        else:
            # In theory we never reach this point
            pass
        for m in range(resolution):
            for n in range(resolution):
                intermediate[m][n] = rotatedtile[m][n]
        # Write the remaining tiles, by using a slightly different black magic
        for i in range(size):
            for j in range(size):
                node = placement[i][j]
                tile = tiles[node]

                if i == 0 and j == 0:
                    # No need to write the first tile, it is already written
                    continue
                elif i != 0:
                    # If we are not on the first row, we can align the tile based on the upper tile
                    border = tuple(
                        intermediate[i * resolution - 1][j * resolution + n]
                        for n in range(resolution)
                    )
                    action = borders[node].index(border)
                elif j != 0:
                    # If we are on the first row, we can align the tile based on the left tile
                    border = tuple(
                        intermediate[i * resolution + m][j * resolution - 1]
                        for m in range(resolution)
                    )
                    action = (
                        borders[node].index(border) + 4
                    ) % 8  # This comes from the order of the borders in borders[node], and it is very magic

                for m in range(resolution):
                    for n in range(resolution):
                        intermediate[i * resolution + m][
                            j * resolution + n
                        ] = self.transform(tile, action)[m][n]
        # Remove the borders of each tile
        image = [[""] * size * (resolution - 2) for _ in range(size * (resolution - 2))]
        ii = 0
        for i in range(size * resolution):
            if i % resolution == 0 or i % resolution == resolution - 1:
                continue
            jj = 0
            for j in range(size * resolution):
                if j % resolution == 0 or j % resolution == resolution - 1:
                    continue
                image[ii][jj] = intermediate[i][j]
                jj += 1
            ii += 1
        # We need to convert the image into a tuple so that the lru cache supports it
        image = tuple(tuple(line) for line in image)

        # Shape the lockness monster and store it as a boolean numpy array
        nessie = (
            np.array(
                [
                    list("                  # "),
                    list("#    ##    ##    ###"),
                    list(" #  #  #  #  #  #   "),
                ],
            )
            == "#"
        )

        # You know what ? I am tired now, so nested for-loop it is
        for action in range(8):
            count = 0
            npimage = np.array(self.transform(image, action))

            for i in range(npimage.shape[0] - nessie.shape[0] + 1):
                for j in range(npimage.shape[1] - nessie.shape[1] + 1):
                    # Extract all elements matching nessie position into a 1d array
                    npextract = np.extract(
                        nessie,
                        npimage[i : i + nessie.shape[0], j : j + nessie.shape[1]],
                    )
                    # Only count this as a match if all extracted elements are "#"
                    count += np.all(npextract == "#")

            if count != 0:
                # Yolo assume that there is a single orientation showing nessies
                break

        # Yolo assume that nessies do not overlap
        # The result is the total number of "#" minus the nessies we found
        return np.count_nonzero(npimage == "#") - count * np.count_nonzero(nessie)

    @staticmethod
    @lru_cache(maxsize=None)
    def transform(tile, action):
        """
        Vertically flip then rotate the tile following these rules :

        action = 0 : flip = False and rotation = 0
        action = 1 : flip = True  and rotation = 0
        action = 2 : flip = False and rotation = pi
        action = 3 : flip = True  and rotation = pi
        action = 4 : flip = True  and rotation = pi / 2
        action = 5 : flip = False and rotation = pi / 2
        action = 6 : flip = True  and rotation = 3 * pi / 2
        action = 7 : flip = False and rotation = 3 * pi / 2
        """
        rotation = (action % 4 >= 2) * pi + (action >= 4) * (pi / 2)
        flip = (action % 2 == 0) ^ (action < 4)

        resolution = len(tile)

        flippedtile = [list(line[:: (1 - 2 * flip)]) for line in tile]
        rotatedtile = list()
        for m in range(resolution):
            rotatedtile.append(list())
            for n in range(resolution):
                u = (m * int(cos(rotation)) + n * int(sin(rotation))) + (
                    (1 if int(cos(rotation)) == -1 or int(sin(rotation)) == -1 else 0)
                    * (resolution - 1)
                )
                v = (-m * int(sin(rotation)) + n * int(cos(rotation))) + (
                    (1 if int(sin(rotation)) == +1 or int(cos(rotation)) == -1 else 0)
                    * (resolution - 1)
                )
                rotatedtile[m].append(flippedtile[u][v])

        return tuple(tuple(line) for line in rotatedtile)


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
        == 273
    )
