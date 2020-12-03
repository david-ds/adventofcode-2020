from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        l = [int(x) for x in s.strip().split()]
        s1 = set(l)

        if 1010 in s1:
            if l.count(1010) >= 2:
                return 1010**2
            s1.discard(1010)

        s2 = {2020-x for x in s1}

        k = next(iter(s1 & s2))
        return k * (2020-k)
