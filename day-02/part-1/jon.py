from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        l = s.strip().split("\n")
        return sum(1 for p in l if is_valid(p))


def is_valid(s):
    r, v = s.split(": ")
    n, l = r.split(" ")
    a, b = n.split("-")
    return int(a) <= v.count(l) <= int(b)
