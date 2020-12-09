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
                invalid_number = xmas[i + self.preamble_size]

        i = 0
        j = 0
        while True:
            if i == j:
                j += 1

            # Do not build a set here, it is way faster to keep the list
            local_sum = sum(xmas[i : j + 1])
            if local_sum == invalid_number:
                return min(xmas[i : j + 1]) + max(xmas[i : j + 1])
            elif local_sum < invalid_number:
                j += 1
            elif local_sum > invalid_number:
                i += 1

    @staticmethod
    def isvalid(target, previous):
        for i in range(len(previous) - 1):
            if target - previous[i] in previous[i + 1 :]:
                return True

        return False
