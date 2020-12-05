from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        values = set()
        for line in s.split('\n'):
            row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
            column = int(line[7:].replace('L', '0').replace('R', '1'), 2)
            values.add(row * 8 + column)
        for i in range(2**10):
            if i not in values and i - 1 in values and i+1 in values:
                return i
