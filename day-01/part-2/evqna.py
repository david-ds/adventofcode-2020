from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def run(self, s):
        entries = [int(line) for line in s.split()]
        for a in entries:
            for b in entries:
                for c in entries:
                    if a + b + c == 2020:
                        return a * b * c
