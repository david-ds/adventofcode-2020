from collections import Counter

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        N_DAYS = 100
        black_hexs = self.parse_start_grid(s)

        for _ in range(N_DAYS):
            n_neighbors = Counter(
                neighbor
                for hex_coord in black_hexs
                for neighbor in self.get_neighbors(*hex_coord)
            )
            black_hexs = {
                hex_coord
                for hex_coord, n in n_neighbors.items()
                if (hex_coord not in black_hexs and n == 2)
                or (hex_coord in black_hexs and n in [1, 2])
            }
        return len(black_hexs)

    @staticmethod
    def get_neighbors(x, y):
        yield x + 2, y
        yield x - 2, y
        yield x + 1, y + 1
        yield x + 1, y - 1
        yield x - 1, y + 1
        yield x - 1, y - 1

    @classmethod
    def parse_start_grid(cls, s):
        black_hexs = set()
        for line in s.splitlines():
            hex_coord = cls.parse_line(line)
            if hex_coord in black_hexs:
                black_hexs.remove(hex_coord)
            else:
                black_hexs.add(hex_coord)
        return black_hexs

    @staticmethod
    def parse_line(line):
        return (
            2 * line.count("w")
            - line.count("nw")
            - line.count("sw")
            - 2 * line.count("e")
            + line.count("ne")
            + line.count("se"),
            line.count("s") - line.count("n"),
        )


def test_thore():
    """
    Run `python -m pytest ./day-24/part-2/thore.py` to test the submission.
    """
    assert (
        ThoreSubmission().run(
            """sesenwnenenewseeswwswswwnenewsewsw
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
