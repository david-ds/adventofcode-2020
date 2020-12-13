from tool.runners.python import SubmissionPy

import math
class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.split("\n")
        t0 = int(lines[0])
        numbers = [int(x) for x in lines[1].split(",") if x != "x"]
        candidates = dict()
        for n in numbers:
            x = math.ceil(t0/n)
            candidates[n] = x*n

        bus = min(candidates.keys(), key=lambda x:candidates[x])
        return bus * (candidates[bus] - t0)
        


