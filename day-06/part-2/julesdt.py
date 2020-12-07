import collections
from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        group_answers = collections.defaultdict(int)
        number_of_people = 0
        total = 0
        for line in s.split('\n'):
            if len(line) == 0:
                for x in group_answers.keys():
                    if group_answers[x] == number_of_people:
                        total += 1
                group_answers = collections.defaultdict(int)
                number_of_people = 0
                continue
            for letter in line:
                group_answers[letter] += 1
            number_of_people += 1
        for x in group_answers.keys():
            if group_answers[x] == number_of_people:
                total += 1
        return total
