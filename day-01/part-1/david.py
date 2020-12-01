from tool.runners.python import SubmissionPy

from collections import defaultdict

class DavidSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        counter = defaultdict(int)
        for x in s.split("\n"):
            counter[int(x)] += 1

        # special case for 1010
        if counter[1010] >= 2 :
            return 1010*1010

        del counter[1010]

        for i in counter.keys():
            j = 2020-i
            if j in counter.keys():
                return i*j
