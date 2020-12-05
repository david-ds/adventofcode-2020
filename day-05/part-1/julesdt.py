from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        max_value = 0
        for line in s.split('\n'):
            row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
            column = int(line[7:].replace('L', '0').replace('R', '1'), 2)
            max_value = max(row * 8 + column, max_value)
        return max_value
