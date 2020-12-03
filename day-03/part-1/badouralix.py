from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0
        position = 0

        for line in s.split():
            if line[position] == "#":
                result += 1
            position = (position + 3) % len(line)

        return result
