from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        adapters = [0] + sorted([int(line) for line in s.splitlines()])
        n_adapters = len(adapters)

        n_combinations_from = [0 for i in range(n_adapters)]
        n_combinations_from[-1] = 1
        for i in range(n_adapters - 2, -1, -1):
            j = i + 1
            while j < n_adapters and adapters[j] - adapters[i] <= 3:
                n_combinations_from[i] += n_combinations_from[j]
                j += 1

        return n_combinations_from[0]


def test_day_10():
    s = """16
10
15
5
1
11
7
19
6
12
4"""
    assert ThoreSubmission().run(s) == 8