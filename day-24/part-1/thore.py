from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        black_hexs = set()
        for line in s.splitlines():
            hex_coord = self.parse_line(line)
            if hex_coord in black_hexs:
                black_hexs.remove(hex_coord)
            else:
                black_hexs.add(hex_coord)
        return len(black_hexs)

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
    Run `python -m pytest ./day-24/part-1/thore.py` to test the submission.
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
        == 10
    )
