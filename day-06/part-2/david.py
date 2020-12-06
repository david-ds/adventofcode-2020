from tool.runners.python import SubmissionPy

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        groups = s.split("\n\n")
        total = 0
        for group in groups:
            answers_per_person = (set(x) for x in group.split("\n"))
            total += len(set.intersection(*answers_per_person))

        return total

