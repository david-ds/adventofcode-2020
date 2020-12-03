from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.split("\n")
        x, y = 0, 0
        max_y = len(s[0])
        max_x = len(s)
        N = 0
        while x < max_x:
            if s[x][y] == "#":
                N += 1
            x += 1
            y = (y + 3) % max_y
        return N
