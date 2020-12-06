from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        values = {int(v) for v in input.split("\n")}
        for v in values:
            if 2020 - v in values:
                return v * (2020 - v)
