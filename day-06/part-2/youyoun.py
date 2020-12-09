from tool.runners.python import SubmissionPy
from collections import Counter


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        groups = [(x.replace("\n", ""), x.count('\n') + 1) for x in s.split("\n\n")]
        acc = 0
        for g in groups:
            acc += len([v for k, v in Counter(g[0]).items() if v == g[1]])
        return acc
