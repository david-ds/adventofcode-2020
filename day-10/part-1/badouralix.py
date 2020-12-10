from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        chain = sorted(map(int, s.split()))
        differences = {1: 0, 2: 0, 3: 1}

        differences[chain[0] - 0] = 1
        for i in range(1, len(chain)):
            differences[chain[i] - chain[i - 1]] += 1

        return differences[1] * differences[3]
