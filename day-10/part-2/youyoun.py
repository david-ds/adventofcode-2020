from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = sorted(map(int, s.splitlines()))
        p = {0: 1}
        for i in s:
            p[i] = p.get(i - 1, 0) + p.get(i - 2, 0) + p.get(i - 3, 0)
        return p[s[-1]]
