from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        groups = s.strip().split("\n\n")

        return sum(len(answers(g)) for g in groups)


def answers(group):
    lines = group.split("\n")
    s = set(lines[0])
    for i in range(1, len(lines)):
        s.intersection_update(set(lines[i]))
    return s
