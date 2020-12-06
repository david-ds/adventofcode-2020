from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        sum_groups = 0
        for group in s.strip().split('\n\n'):
            sum_groups += len(set(group.replace('\n', '')))
        return sum_groups
