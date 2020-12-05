from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        return max(self.get_seat_id(line) for line in s.split("\n"))

    def get_seat_id(self, bsp):
        binary_string = "".join(["1" if c in {"B", "R"} else "0" for c in bsp.strip()])
        n = int(binary_string, 2)

        row = n >> 3
        col = n & 0b111

        return row * 8 + col


def test_day5():
    assert ThoreSubmission().get_seat_id("BFFFBBFRRR") == 567
    assert ThoreSubmission().get_seat_id("FFFBBBFRRR") == 119
    assert ThoreSubmission().get_seat_id("BBFFBBFRLL") == 820