from tool.runners.python import SubmissionPy

import numpy as np

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        l = [int(x) for x in s.split("\n")]
        l = [0] + l
        a = np.array(l, dtype="int64")
        a = np.sort(a)
        diff = a[1:] - a[:-1]
        return np.sum(diff == 1) * (np.sum(diff == 3) + 1)
