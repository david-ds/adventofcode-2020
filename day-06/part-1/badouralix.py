from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        groups = s.split("\n\n")
        result = 0

        for group in groups:
            result += len(set(group.replace("\n", "")))

        return result
