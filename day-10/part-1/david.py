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
        diffs = defaultdict(int)
        for i in range(len(l)-1):
            # assert(l[i+1]-l[i] in {1,2,3})
            diffs[l[i+1]-l[i]] += 1

        return diffs[3] * diffs[1]
