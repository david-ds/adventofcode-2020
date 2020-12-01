from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        entries = {int(x) for x in s.split("\n")}
        for i in entries:
            j = 2020-i
            if j in entries:
                return i*j
