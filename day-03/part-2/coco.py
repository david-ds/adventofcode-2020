from tool.runners.python import SubmissionPy
import math


class CocoSubmission(SubmissionPy):
    def trees(self, s, inc_x, inc_y):
        x, y = 0, 0
        max_x = len(s)
        max_y = len(s[0])
        N = 0
        while True:
            if s[x][y] == "#":
                N += 1
            x += inc_x
            if x >= max_x:
                break
            y = (y + inc_y) % max_y
        return N

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        s = s.split("\n")
        results = [
            self.trees(s, inc_x, inc_y)
            for inc_x, inc_y in [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
        ]
        return math.prod(results)
