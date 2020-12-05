from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s = s.strip().replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")

        return max(int(x, 2) for x in s.split("\n"))
