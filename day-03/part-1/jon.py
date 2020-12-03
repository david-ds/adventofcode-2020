from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        m = list(s.strip().split("\n"))
        ny = len(m)
        nx = len(m[0])
        return sum(1 for y in range(1, ny) if m[y][(3*y) % nx] == "#")
