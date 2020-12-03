from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.split('\n')
        moves = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
        height = len(lines)
        width = len(lines[0])
        total_counter = 1
        for move in moves:
            i = 0
            j = 0
            counter = 0
            while i < height:
                if lines[i][j] == '#':
                    counter += 1
                i = i + move[0]
                j = (j + move[1]) % width
            total_counter *= counter
        return total_counter
