from tool.runners.python import SubmissionPy

from collections import defaultdict

class DavidSubmission(SubmissionPy):
    TARGET = 30_000_000

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        starting_numbers = [int(x) for x in s.split(",")]
        d = dict()
        for i,n in enumerate(starting_numbers):
            if n in d:
                d[n] = (i, d[n][0])
            else:
                d[n] = (i,None)

        i = len(starting_numbers)
        last_number = starting_numbers[i-1]
        for i in range(len(starting_numbers), self.TARGET):
            j1,j2 = d.get(last_number, (None,None))

            if j2 is not None:
                # it appeared before
                last_number = j1-j2
            else:
                last_number = 0

            j1,_ = d.get(last_number, (None,None))
            d[last_number] = (i,j1)

        return last_number
