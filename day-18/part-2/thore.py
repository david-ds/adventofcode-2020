import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = re.sub(
            r"(\d+)", r"Int(\1)", s.translate(str.maketrans({"+": "*", "*": "+"}))
        )
        return sum([int(eval(line)) for line in s.splitlines()])


class Int(int):
    """Custom class for integers where * is addition and + is multiplication so
    that addition have precedence over multiplication"""

    def __mul__(self, other):
        return Int(int(self) + int(other))

    def __add__(self, other):
        return Int(int(self) * int(other))


def test_day18_part2():
    assert ThoreSubmission().run("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert ThoreSubmission().run("2 * 3 + (4 * 5)") == 46
    assert ThoreSubmission().run("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert ThoreSubmission().run("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert (
        ThoreSubmission().run("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
        == 23340
    )
