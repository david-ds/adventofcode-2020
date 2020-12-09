from tool.runners.python import SubmissionPy
from collections import Counter


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        groups = [x.replace("\n", "") for x in s.split("\n\n")]
        acc = 0
        for g in groups:
            acc += len(set(g))
        return acc
