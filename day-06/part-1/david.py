from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        groups = s.split("\n\n")
        return sum(len(set(group.replace("\n", ""))) for group in groups)
