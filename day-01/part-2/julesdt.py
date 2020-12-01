from tool.runners.python import SubmissionPy
import itertools


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        for pair in itertools.combinations(map(int, s.split('\n')), 3):
            if pair[0] + pair[1] + pair[2] == 2020:
                return pair[0] * pair[1] * pair[2]
