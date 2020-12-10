from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        adapters = sorted([int(line) for line in s.splitlines()])
        diffs = [j - i for i, j in zip(adapters, adapters[1:])]
        return (diffs.count(1) + 1) * (diffs.count(3) + 1)
