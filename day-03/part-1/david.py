from tool.runners.python import SubmissionPy

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        slopes = [list(line) for line in s.split("\n")]
        x, y = 0, 0
        trees = 0
        while y < len(slopes):
            if slopes[y][x%len(slopes[0])] == "#":
                trees += 1
            y += 1
            x += 3
        return trees

