from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def is_valid(self, password_entry):
        policy, c, pwd = password_entry.split()
        c = c[0]
        c_min, c_max = map(int, policy.split('-'))
        pwd_set = ''.join(sorted(pwd))
        return c * c_min in pwd_set and c * (c_max + 1) not in pwd_set

    def run(self, s):
        return sum(1 for entry in s.splitlines() if self.is_valid(entry))
