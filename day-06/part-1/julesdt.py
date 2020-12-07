from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        group_answers = set()
        total = 0
        for line in s.split('\n'):
            if len(line) == 0:
                total += len(group_answers)
                group_answers = set()
            for letter in line:
                group_answers.add(letter)
        return total + len(group_answers)
