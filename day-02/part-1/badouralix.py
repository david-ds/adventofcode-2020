from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n"):
            mincount, maxcount, char, password = (
                line.replace("-", " ").replace(":", " ").split()
            )
            count = password.count(char)
            if count >= int(mincount) and count <= int(maxcount):
                result += 1

        return result
