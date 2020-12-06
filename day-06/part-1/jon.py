from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        groups = s.strip().split("\n\n")

        return sum(len(set(g.replace("\n", ""))) for g in groups)
