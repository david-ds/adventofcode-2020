from tool.runners.python import SubmissionPy

import math

class DavidSubmission(SubmissionPy):

    def ski(self, slopes, offset):
        x, y = 0, 0
        trees = 0
        while y < len(slopes):
            if slopes[y][x%len(slopes[0])] == "#":
                trees += 1
            x, y = x + offset[0], y + offset[1]
        return trees

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        slopes = [list(line) for line in s.split("\n")]
        results = (self.ski(slopes, offset) for offset in {(1,1), (3,1), (5,1), (7,1), (1,2)})
        return math.prod(results)
