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
    @staticmethod
    def get_neighbors(x, y, with_itself=False):
        if with_itself:
            yield x, y
        yield x - 1, y
        yield x - 0.5, y + 1
        yield x + 0.5, y + 1
        yield x + 1, y
        yield x + 0.5, y - 1
        yield x - 0.5, y - 1

    def run(self, s, nb_days=100):
        black_tiles = set()
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

            if (x, y) in black_tiles:
                black_tiles.remove((x, y))
            else:
                black_tiles.add((x, y))

        for _ in range(nb_days):
            new_black_tiles = set()
            for x, y in set.union(
                *[
                    set(self.get_neighbors(xx, yy, with_itself=True))
                    for xx, yy in black_tiles
                ]
            ):
                neighbors = self.get_neighbors(x, y)
                nb_black_tiles = 0
                for xxx, yyy in neighbors:
                    if (xxx, yyy) in black_tiles:
                        nb_black_tiles += 1
                        if nb_black_tiles >= 3:
                            break

                if (x, y) in black_tiles:
                    if nb_black_tiles == 1 or nb_black_tiles == 2:
                        new_black_tiles.add((x, y))
                elif nb_black_tiles == 2:
                    new_black_tiles.add((x, y))

            black_tiles = new_black_tiles

        return len(black_tiles)


def test_th_ch():
    """
    Run `python -m pytest ./day-24/part-2/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
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
