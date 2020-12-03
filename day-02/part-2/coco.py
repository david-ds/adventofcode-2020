from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        inputs = [l.strip().split(" ") for l in s.split("\n")]
        N = 0
        for policy, letter, password in inputs:
            a, b = policy.split("-")
            a, b = int(a) - 1, int(b) - 1
            letter = letter[0]
            if (password[a] == letter) != (password[b] == letter):
                N += 1
        return N
