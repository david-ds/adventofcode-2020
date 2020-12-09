from collections import deque
from itertools import combinations
from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s, maxlen=25):
        """
        :param s: input in string format
        :return: solution flag
        """
        numbers = [int(line) for line in s.splitlines()]
        for i in range(maxlen, len(numbers)):
            n = numbers[i]
            previous = numbers[i - maxlen : i]
            if not any(n - m in previous and n - m != m for m in previous):
                return n


def test_day9_part1():
    s = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    assert ThoreSubmission().run(s, maxlen=5) == 127