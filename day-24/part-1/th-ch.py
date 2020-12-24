from tool.runners.python import SubmissionPy

WHITE = 0
BLACK = 1
DIRECTIONS = {
    "e": (-1, 0),  # (x, y) with axes right/bottom
    "se": (-0.5, 1),
    "sw": (0.5, 1),
    "w": (1, 0),
    "nw": (0.5, -1),
    "ne": (-0.5, -1),
}


class ThChSubmission(SubmissionPy):
    def run(self, s):
        flipped_tiles = {}
        for line in s.split("\n"):
            i = 0
            x, y = (0, 0)  # ref
            while i < len(line):
                if line[i] == "s" or line[i] == "n":
                    direction = line[i : i + 2]
                    i += 2
                else:
                    direction = line[i]
                    i += 1

                dx, dy = DIRECTIONS[direction]
                x += dx
                y += dy

            flipped_tiles[(x, y)] = (flipped_tiles.get((x, y), WHITE) + 1) % 2

        return sum(tile == BLACK for tile in flipped_tiles.values())


def test_th_ch():
    """
    Run `python -m pytest ./day-24/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
seeswwswswwnenewsewsw
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
