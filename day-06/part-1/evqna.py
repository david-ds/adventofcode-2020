from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def yes_count(self, group):
        return len(set(group.replace('\n', '')))

    def run(self, s):
        return sum(self.yes_count(group) for group in s.split('\n\n'))
