from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split('\n')
        i = 0
        j = 0
        height = len(lines)
        width = len(lines[0])
        counter = 0
        while i < height:
            if lines[i][j] == '#':
                counter += 1
            i = i + 1
            j = (j + 3) % width
        return counter
