from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        sum_groups = 0
        for group in s.strip().split('\n\n'):
            all_yes = set('abcdefghijklmnopqrstuvwxyz')
            for p in group.split('\n'):
                all_yes = all_yes.intersection(p)
            sum_groups += len(all_yes)
        return sum_groups
