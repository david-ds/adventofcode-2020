from tool.runners.python import SubmissionPy

from collections import defaultdict


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        flips = defaultdict(int)

        for line in s.split("\n"):
            # Flatten the input line to ease the for loop below
            line = (
                line.replace("ne", "a")
                .replace("nw", "b")
                .replace("se", "c")
                .replace("sw", "d")
            )

            # Figure out the target tile by projecting it within the regular cartesian coordinates
            tile = (0, 0)
            for char in line:
                if char == "e":
                    tile = (tile[0] + 1, tile[1])
                elif char == "w":
                    tile = (tile[0] - 1, tile[1])
                elif char == "a":
                    tile = (tile[0], tile[1] + 1)
                elif char == "b":
                    tile = (tile[0] - 1, tile[1] + 1)
                elif char == "c":
                    tile = (tile[0] + 1, tile[1] - 1)
                elif char == "d":
                    tile = (tile[0], tile[1] - 1)

            # Store the flipping action
            flips[tile] += 1

        return sum(1 for tile in flips if flips[tile] % 2 == 1)


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
        == 10
    )
