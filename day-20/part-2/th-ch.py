from tool.runners.python import SubmissionPy

import math
import copy
import re

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class ThChSubmission(SubmissionPy):
    def neighbors(self, x, y, side):
        neighbors = []  # neighbor_x, neighbor_y, side for x/y, side for neighbor
        for n_x, n_y in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]:
            if n_x >= 0 and n_x < side and n_y >= 0 and n_y < side:
                side_index, side_neighbor = (
                    ((DOWN, UP) if n_y > y else (UP, DOWN))
                    if n_x == x
                    else ((RIGHT, LEFT) if n_x > x else (LEFT, RIGHT))
                )
                neighbors.append((n_x, n_y, side_index, side_neighbor))

        return neighbors

    def backtracking(self, mapping, mapping_by_pos, tiles, x, y):
        if len(mapping) == len(tiles):
            # finished
            return mapping_by_pos, mapping

        tile_ids_to_try = []
        neighbors = self.neighbors(x, y, len(mapping_by_pos))
        for tile_id in tiles:
            if tile_id in mapping:
                continue
            for tile in tiles[tile_id]:
                all_neighbors_ok = True
                for n_x, n_y, side_index, side_neighbor in neighbors:
                    if mapping_by_pos[n_y][n_x] is not None:
                        n_tile = mapping[mapping_by_pos[n_y][n_x]]
                        if n_tile[side_neighbor] != tile[side_index]:
                            all_neighbors_ok = False
                            break
                if all_neighbors_ok:
                    # Possible candidate
                    tile_ids_to_try.append((tile_id, tile))

        if not tile_ids_to_try:
            return None, None

        while tile_ids_to_try:
            tile_id_to_try, tile = tile_ids_to_try.pop(0)

            mapping[tile_id_to_try] = tile
            mapping_by_pos[y][x] = tile_id_to_try

            next_x, next_y = next(
                (
                    (xx, yy)
                    for yy in range(len(mapping_by_pos))
                    for xx in range(len(mapping_by_pos[yy]))
                    if mapping_by_pos[yy][xx] is None
                ),
                (None, None),
            )
            if next_x is None:
                # finished
                return mapping_by_pos, mapping

            new_mapping_by_pos = copy.deepcopy(mapping_by_pos)
            new_mapping = copy.deepcopy(mapping)

            new_new_mapping_by_pos, new_new_mapping = self.backtracking(
                new_mapping, new_mapping_by_pos, tiles, next_x, next_y
            )

            if new_new_mapping_by_pos is None:
                # revert
                del mapping[tile_id_to_try]
                mapping_by_pos[y][x] = None
            elif len(new_new_mapping) == len(tiles):
                # finished
                return new_new_mapping_by_pos, new_new_mapping

        return None, None

    def invert_side(self, side, image_size):
        return frozenset(image_size - 1 - p for p in side)

    def flip_vertical(self, tile, image_size):
        up, down, left, right, image = tile
        return (
            self.invert_side(up, image_size),
            self.invert_side(down, image_size),
            right,
            left,
            self.flip_matrix_vertical(image),
        )

    def rotate_matrix(self, m):
        return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]

    def flip_matrix_vertical(self, m):
        return [line[::-1] for line in m]

    def run(self, s):
        tiles = {}  # {[tile_id]: [(up, down, left, right)]}
        inline_images = {}

        stringified_tiles = s.split("\n\n")
        for stringified_tile in stringified_tiles:
            lines = stringified_tile.split("\n")
            tile_id = int(lines[0].replace("Tile ", "")[:-1])
            # Inline the image without borders
            inline_image = [[c for c in line[1:-1]] for line in lines[2:-1]]
            # Each tile side is represented with a set
            image_size = len(lines) - 1
            up = frozenset(i for i, pixel in enumerate(lines[1]) if pixel == "#")
            down = frozenset(i for i, pixel in enumerate(lines[-1]) if pixel == "#")
            left = frozenset(i for i in range(image_size) if lines[i + 1][0] == "#")
            right = frozenset(i for i in range(image_size) if lines[i + 1][-1] == "#")
            simple_tiles = [
                # Normal
                (up, down, left, right, inline_image),
                # Rotated
                (
                    self.invert_side(left, image_size),
                    self.invert_side(right, image_size),
                    down,
                    up,
                    self.rotate_matrix(
                        self.rotate_matrix(self.rotate_matrix(inline_image))
                    ),
                ),
                (
                    self.invert_side(down, image_size),
                    self.invert_side(up, image_size),
                    self.invert_side(right, image_size),
                    self.invert_side(left, image_size),
                    self.rotate_matrix(self.rotate_matrix(inline_image)),
                ),
                (
                    right,
                    left,
                    self.invert_side(up, image_size),
                    self.invert_side(down, image_size),
                    self.rotate_matrix(inline_image),
                ),
            ]
            tiles[tile_id] = simple_tiles.copy()
            # Flip
            for simple_tile in simple_tiles:
                # Vertical flip is enough to have everything due to the rotations
                vertical = self.flip_vertical(simple_tile, image_size)
                if vertical not in tiles[tile_id]:
                    tiles[tile_id].append(vertical)

        side = int(math.sqrt(len(tiles)))
        mapping = {}  #  {[tile_id]: (x,y)}
        mapping_by_pos = [[None for _ in range(side)] for _ in range(side)]
        mapping_by_pos, mapping = self.backtracking(
            mapping, mapping_by_pos, tiles, 0, 0
        )

        # Generate the image
        initial_matrix = []
        for line in mapping_by_pos:
            for i in range(image_size - 2):
                matrix_line = []
                for tile_id in line:
                    matrix_line += mapping[tile_id][-1][i]
                initial_matrix.append(matrix_line)

        matrixes = [initial_matrix]
        for _ in range(3):
            m = matrixes[-1]
            matrixes.append(self.rotate_matrix(m))
        for m in matrixes.copy():
            matrixes.append(self.flip_matrix_vertical(m))

        inline_images = ["".join("".join(line) for line in m) for m in matrixes]
        nb_matches = {}
        width = int(math.sqrt(len(inline_images[0])))
        inline_pattern_regex = (
            ".*"
            + "(#|O).{{{}}}(#|O)....((#|O){{2}})....((#|O){{2}})....((#|O){{3}}).{{{}}}(#|O)..(#|O)..(#|O)..(#|O)..(#|O)..(#|O)".format(
                width - 19, width - 19
            )
            + ".*"
        )
        regex = re.compile(inline_pattern_regex)

        for j, inline_image in enumerate(inline_images):
            subimages = [inline_image]

            while len(subimages) > 0:
                subimage = subimages.pop(0)
                match = regex.match(subimage)
                if match is not None:
                    for group in range(1, 15):
                        start, end = match.span(group)
                        replacement = "O" * (end - start)
                        inline_image = replacement.join(
                            [inline_image[:start], inline_image[end:]]
                        )
                    if inline_images[j] in nb_matches:
                        nb_matches[inline_image] = nb_matches[inline_images[j]]
                        del nb_matches[inline_images[j]]
                    inline_images[j] = inline_image

                    subimages.append(inline_image[: match.end(14) - 1])

                    if inline_image not in nb_matches:
                        nb_matches[inline_image] = 0
                    nb_matches[inline_image] += 1

        current_max = 0
        current_score = 0

        for image in nb_matches:
            if nb_matches[image] > current_max:
                current_max = nb_matches[image]
                current_score = image.count("#")

        return current_score
