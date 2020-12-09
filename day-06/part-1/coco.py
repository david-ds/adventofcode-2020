from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        groups = s.split("\n\n")
        answer = sum([len(set(g.replace("\n", ""))) for g in groups])
        return answer
