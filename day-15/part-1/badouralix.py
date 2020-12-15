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
        current = start[-1]

        for i in range(len(start) - 1, 2020 - 1):
            if current in memory:
                j = memory[current]
                memory[current] = i
                current = i - j
            else:
                memory[current] = i
                current = 0

        return current
