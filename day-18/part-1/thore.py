import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = re.sub(r"(\d+)", r"Int(\1)", s.replace("+", "/"))
        return sum([eval(line) for line in s.splitlines()])


class Int(int):
    """Custom class for integers where / is addition so that addition and
    multiplication have the same precedence"""

    def __mul__(self, other):
        return Int(int(self) * int(other))

    def __truediv__(self, other):
        return Int(int(self) + int(other))


def test_day18_part1():
    assert ThoreSubmission().run("2 * 3 + (4 * 5)") == 26
    assert ThoreSubmission().run("5 + (8 * 3 + 9 + 3 * 4 * 3) ") == 437
    assert ThoreSubmission().run("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert (
        ThoreSubmission().run("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
        == 13632
    )
