from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        s = s.strip().replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")

        seats = set(int(x, 2) for x in s.split("\n"))
        n_min = min(seats)
        n_max = max(seats)

        return next(iter(set(range(n_min, n_max+1)) - seats))
