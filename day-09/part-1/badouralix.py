from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def __init__(self):
        self.preamble_size = 25

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        xmas = list(map(int, s.split()))

        for i in range(len(xmas) - self.preamble_size):
            if not self.isvalid(
                xmas[i + self.preamble_size], xmas[i : i + self.preamble_size]
            ):
                return xmas[i + self.preamble_size]

    @staticmethod
    def isvalid(target, previous):
        for i in range(len(previous) - 1):
            if target - previous[i] in previous[i + 1 :]:
                return True

        return False
