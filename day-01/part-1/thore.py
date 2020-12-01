from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        numbers = set([int(n) for n in s.split()])
        target = 2020

        for n in numbers:
            if target - n in numbers:
                return n * (target - n)

        raise ValueError("Invalid input")
