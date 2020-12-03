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
            low, high = policy.split("-")
            low, high = int(low), int(high)
            letter = letter[0]
            occurences = password.count(letter)
            if low <= occurences <= high:
                N += 1
        return N
