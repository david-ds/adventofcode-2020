from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def all_yes(self, group):
        answered_by_all = set('abcdefghijklmnopqrstuvwxyz')
        for member in group:
            answered_by_all.intersection_update(set(member))
        return len(answered_by_all)

    def run(self, s):
        groups = [group.split() for group in s.split('\n\n')]
        return sum(self.all_yes(g) for g in groups)
