from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        ranges, my_ticket, other_tickets = s.split("\n\n")
        valid_ranges = self.parse_ranges(ranges)

        error_rate = 0
        for ticket in other_tickets.splitlines()[1:]:
            values = [int(c) for c in ticket.split(",")]
            error_rate += sum(v for v in values if not self.is_valid(valid_ranges, v))

        return error_rate

    @staticmethod
    def parse_ranges(ranges_str):
        ranges = []
        for line in ranges_str.split("\n"):
            line_ranges = line.split(": ")[1].split(" or ")
            # TODO: merging overlapping ranges would be more efficient then
            ranges.extend([tuple(map(int, lr.split("-"))) for lr in line_ranges])
        return ranges

    @staticmethod
    def is_valid(valid_ranges, v):
        return any(x <= v <= y for x, y in valid_ranges)


def test_day16_part1():
    assert (
        ThoreSubmission().run(
            """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
        )
        == 71
    )


def test_parse_ranges():
    assert (
        ThoreSubmission.parse_ranges(
            """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50"""
        )
        == [(1, 3), (5, 7), (6, 11), (33, 44), (13, 40), (45, 50)]
    )
