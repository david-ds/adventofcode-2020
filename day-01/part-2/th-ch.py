from itertools import combinations

from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        values = {int(v) for v in input.split("\n")}
        for v1, v2 in combinations(values, 2):
            if 2020 - v1 - v2 in values:
                return v1 * v2 * (2020 - v1 - v2)
