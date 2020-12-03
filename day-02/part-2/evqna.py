from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def is_valid(self, password_entry):
        policy, c, pwd = password_entry.split()
        c = c[0]
        pos = map(int, policy.split('-'))
        return sum(1 for p in pos if pwd[p-1] == c) == 1

    def run(self, s):
        return sum(1 for entry in s.splitlines() if self.is_valid(entry))
