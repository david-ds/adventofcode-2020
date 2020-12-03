from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def run(self, s):
        entries = [int(line) for line in s.split()]
        for a in entries:
            for b in entries:
                if a + b == 2020:
                    return a * b
