from tool.runners.python import SubmissionPy
from collections import Counter

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        groups = s.split("\n\n")
        sum = 0
        for g in groups:
            persons = g.split("\n")
            answer_sets = [set(p) for p in persons]
            sum += len(set.intersection(*answer_sets))
        return sum
