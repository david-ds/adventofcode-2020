from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        l = [int(x) for x in s.strip().split()]
        n = len(l)

        for i in range(n):
            for j in range(i):
                if l[i] + l[j] > 2020:
                    continue
                for k in range(j):
                    if l[i] + l[j] + l[k] == 2020:
                        return str(l[i] * l[j] * l[k])
