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

        for i in range(len(numbers)):
            range_sum = numbers[i]
            j = i + 1
            while range_sum < invalid_number:
                range_sum += numbers[j]
                j += 1
            if range_sum == invalid_number:
                return min(numbers[i:j]) + max(numbers[i:j])

    @staticmethod
    def find_invalid_number(numbers, maxlen):
        for i in range(maxlen + 1, len(numbers)):
            if numbers[i] not in [
                x + y for x, y in combinations(numbers[i - maxlen : i], 2)
            ]:
                return numbers[i]


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