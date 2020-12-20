from tool.runners.python import SubmissionPy

import math
import copy

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class ThChSubmission(SubmissionPy):
    def neighbors(self, x, y, side):
        neighbors = []  # neighbor_x, neighbor_y, side for x/y, side for neighbor
        for n_x, n_y in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]:
            if n_x >= 0 and n_x < side and n_y >= 0 and n_y < side:
                sides = (
                    ((DOWN, UP) if n_y > y else (UP, DOWN))
                    if n_x == x
                    else ((RIGHT, LEFT) if n_x > x else (LEFT, RIGHT))
                )
                neighbors.append((n_x, n_y, sides[0], sides[1]))

        return neighbors

    def invert_side(self, side, image_size):
        return frozenset(image_size - 1 - p for p in side)

    def run(self, s):
        tiles = {}  # {[tile_id]: [(up, down, left, right)]}

        stringified_tiles = s.split("\n\n")
        for stringified_tile in stringified_tiles:
            lines = stringified_tile.split("\n")
            tile_id = int(lines[0].replace("Tile ", "")[:-1])
            # Each tile side is represented with a set
            image_size = len(lines) - 1
            up = frozenset(i for i, pixel in enumerate(lines[1]) if pixel == "#")
            down = frozenset(i for i, pixel in enumerate(lines[-1]) if pixel == "#")
            left = frozenset(i for i in range(image_size) if lines[i + 1][0] == "#")
            right = frozenset(i for i in range(image_size) if lines[i + 1][-1] == "#")
            tiles[tile_id] = [
                # Normal
                (up, down, left, right),
                # Rotated
                (
                    self.invert_side(left, image_size),
                    self.invert_side(right, image_size),
                    down,
                    up,
                ),
                (
                    self.invert_side(down, image_size),
                    self.invert_side(up, image_size),
                    self.invert_side(right, image_size),
                    self.invert_side(left, image_size),
                ),
                (
                    right,
                    left,
                    self.invert_side(up, image_size),
                    self.invert_side(down, image_size),
                ),
                # flipped
                (
                    self.invert_side(up, image_size),
                    self.invert_side(down, image_size),
                    right,
                    left,
                ),
                (
                    down,
                    up,
                    self.invert_side(left, image_size),
                    self.invert_side(right, image_size),
                ),
            ]

        tile_id_by_side = {}
        for tile_id in tiles:
            for tile in [tiles[tile_id][0], tiles[tile_id][2]]:
                for side in tile:
                    if side not in tile_id_by_side:
                        tile_id_by_side[side] = set()
                    tile_id_by_side[side].add(tile_id)

        isolated_sides_by_tile_id = {}
        corners = []
        for side in tile_id_by_side:
            tile_ids = tile_id_by_side[side]
            if len(tile_ids) == 1:
                tile_id = tile_ids.pop()
                if tile_id not in isolated_sides_by_tile_id:
                    isolated_sides_by_tile_id[tile_id] = [side]
                elif (
                    side not in isolated_sides_by_tile_id[tile_id]
                    and self.invert_side(side, image_size)
                    not in isolated_sides_by_tile_id[tile_id]
                ):
                    isolated_sides_by_tile_id[tile_id].append(side)
                    if len(isolated_sides_by_tile_id[tile_id]) >= 2:
                        corners.append(tile_id)
                        if len(corners) >= 4:
                            break

        return math.prod(corners)
