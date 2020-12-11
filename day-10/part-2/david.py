from tool.runners.python import SubmissionPy

from collections import defaultdict

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        l = sorted([int(x) for x in s.split("\n")])
        l = [0] + l + [l[-1]+3]
        n = len(l)
        cache = [0] * n
        cache[0] = 1
        for i in range(1,n):
            if i-1 >= 0 and l[i] - l[i-1] <= 3:
                cache[i] += cache[i-1]
            if i-2 >= 0 and l[i] - l[i-2] <= 3:
                cache[i] += cache[i-2]
            if i-3 >= 0 and l[i] - l[i-3] <= 3:
                cache[i] += cache[i-3]

        return cache[n-1]
