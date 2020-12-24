from tool.runners.python import SubmissionPy

from collections import defaultdict
from functools import lru_cache


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        flipped_tiles = set()  # Activated tiles
        flipped_neighbors = defaultdict(int)  # Number of activated neighbors per tile

        for line in s.split("\n"):
            # Flatten the input line to ease the for loop below
            line = (
                line.replace("ne", "a")
                .replace("nw", "b")
                .replace("se", "c")
                .replace("sw", "d")
            )

            # Figure out the target tile by projecting it within the regular cartesian coordinates
            tile = (
                line.count("e") - line.count("w") - line.count("b") + line.count("c"),
                line.count("a") + line.count("b") - line.count("c") - line.count("d"),
            )

            # Store the flipping action
            self.flip_tile(tile, flipped_tiles, flipped_neighbors)

        for day in range(1, 101):
            # Save previous state
            backup_tiles = flipped_tiles.copy()
            backup_neighbors = flipped_neighbors.copy()

            # Propagate one step of the game of life
            for tile in backup_neighbors:
                if tile in backup_tiles and (
                    backup_neighbors[tile] == 0 or backup_neighbors[tile] > 2
                ):
                    self.flip_tile(tile, flipped_tiles, flipped_neighbors)
                elif tile not in backup_tiles and backup_neighbors[tile] == 2:
                    self.flip_tile(tile, flipped_tiles, flipped_neighbors)

        return len(flipped_tiles)

    def flip_tile(self, tile, flipped_tiles, flipped_neighbors):
        # Hack to have tile in flipped_neighbors keys
        flipped_neighbors[tile] = flipped_neighbors[tile]

        # Implement the actual flip
        if tile in flipped_tiles:
            flipped_tiles.remove(tile)
            for neighbor in self.neighbors(tile):
                flipped_neighbors[neighbor] -= 1
        else:
            flipped_tiles.add(tile)
            for neighbor in self.neighbors(tile):
                flipped_neighbors[neighbor] += 1

    @staticmethod
    @lru_cache(maxsize=None)
    def neighbors(tile):
        return {
            (tile[0] + 1, tile[1]),
            (tile[0] - 1, tile[1]),
            (tile[0], tile[1] + 1),
            (tile[0] - 1, tile[1] + 1),
            (tile[0] + 1, tile[1] - 1),
            (tile[0], tile[1] - 1),
        }


def test_badouralix():
    """
    Run `python -m pytest ./day-24/part-1/badouralix.py` to test the submission.
    """
    assert (
        BadouralixSubmission().run(
            """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""".strip()
        )
        == 2208
    )
