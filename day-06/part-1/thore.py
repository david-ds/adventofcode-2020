from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        return sum(len(set(answers.replace("\n", ""))) for answers in s.split("\n\n"))