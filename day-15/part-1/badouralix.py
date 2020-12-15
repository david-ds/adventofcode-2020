from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        memory = dict()
        start = [int(n) for n in s.split(",")]

        for i in range(len(start)):
            memory[start[i]] = i
        last = start[-1]

        for i in range(len(start) - 1, 2020 - 1):
            if last in memory:
                j = memory[last]
                memory[last] = i
                last = i - j
            else:
                memory[last] = i
                last = 0

        return last
