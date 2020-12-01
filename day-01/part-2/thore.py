from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        numbers = set([int(n) for n in s.split()])
        target = 2020

        for n1 in numbers:
            for n2 in numbers:
                if target - n1 - n2 in numbers:
                    return n1 * n2 * (target - n1 - n2)

        raise ValueError("Invalid input")