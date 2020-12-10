from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = sorted(map(int, s.splitlines()))
        ones = 1
        threes = 1
        for i in range(len(s) - 1):
            if s[i + 1] - s[i] == 1:
                ones += 1
            elif s[i + 1] - s[i] == 3:
                threes += 1
            elif s[i + 1] - s[i] > 3:
                print("Shit")
                break
        return ones * threes
