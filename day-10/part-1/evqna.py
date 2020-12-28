from tool.runners.python import SubmissionPy

from collections import defaultdict

class EvqnaSubmission(SubmissionPy):

    def count_diffs(self, L):
        prev = 0
        diffs = defaultdict(int)
        for n in L:
            diffs[n - prev] += 1
            prev = n
        return diffs

    def run(self, s):
        adapters = sorted([int(n) for n in s.splitlines()])
        adapters.append(adapters[-1] + 3)
        diffs = self.count_diffs(adapters)
        return diffs[1] * diffs[3]
