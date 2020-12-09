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
        invalid_number = self.find_invalid_number(numbers, maxlen=maxlen)

        i, j = 0, 1
        sum_i_j = numbers[0]  # keep track of sum(numbers[i:j])
        while sum_i_j != invalid_number:
            if sum_i_j < invalid_number:
                sum_i_j += numbers[j]
                j += 1
            elif sum_i_j > invalid_number:
                sum_i_j -= numbers[i]
                i += 1
                # no need to reset j since for i < k < j we have
                # sum(numbers[i:k]) <= sum(numbers[i:j-1]) < invalid_number
        return min(numbers[i:j]) + max(numbers[i:j])

    @staticmethod
    def find_invalid_number(numbers, maxlen):
        for i in range(maxlen, len(numbers)):
            n = numbers[i]
            previous = numbers[i - maxlen : i]
            if not any(n - m in previous and n - m != m for m in previous):
                return n


def test_day9_part2():
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
    assert ThoreSubmission().run(s, maxlen=5) == 62