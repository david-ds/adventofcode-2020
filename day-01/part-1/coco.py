from tool.runners.python import SubmissionPy

from collections import defaultdict

class COCOSubmission(SubmissionPy):

    def run(self, s):
        numbers = [int(n.strip()) for n in s.split("\n") if n.strip() != '']
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                if numbers[i] + numbers[j] == 2020:
                    return numbers[i] * numbers[j]
