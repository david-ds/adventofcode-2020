from tool.runners.python import SubmissionPy

from collections import defaultdict

class DavidSubmission(SubmissionPy):
    PREAMBLE_SIZE = 25

    def find_target(self, data):
        d = defaultdict(int)
        for i in range(self.PREAMBLE_SIZE):
            d[data[i]] += 1

        for n in range(self.PREAMBLE_SIZE, len(data)):
            valid = False
            for k in range(n-self.PREAMBLE_SIZE, n):
                if data[n]-data[k] in d:
                    # handle special case where 2*data[k] = data[n]
                    if 2*data[k] == data[n] and d[data[k]] == 1:
                        continue
                    valid = True
                    break
            if not valid:
                return data[n]

            d[data[n]] = n
            del d[data[n-self.PREAMBLE_SIZE]]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = [int(x.strip()) for x in s.split("\n")]
        return self.find_target(lines)
