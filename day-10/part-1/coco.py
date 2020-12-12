from tool.runners.python import SubmissionPy
from collections import Counter

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        numbers = [int(n) for n in s.split("\n")]
        numbers.append(max(numbers) + 3)
        numbers.append(0)
        numbers = sorted(numbers)
        differences = [b - a for (a, b) in zip(numbers[:-1], numbers[1:])]
        c =  Counter(differences)
        return c[1] * c[3]
