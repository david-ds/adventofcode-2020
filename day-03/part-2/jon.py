from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        m = list(s.strip().split("\n"))
        ny = len(m)
        nx = len(m[0])

        def trees(dx, dy):
            return sum(1 for y in range(dy, ny, dy) if m[y][(dx*(y//dy)) % nx] == "#")

        return trees(1, 1) * trees(3, 1) * trees(5, 1) * trees(7, 1) * trees(1, 2)
