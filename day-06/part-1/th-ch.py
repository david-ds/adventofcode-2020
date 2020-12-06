from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        return sum(len(set(answer.replace("\n", ""))) for answer in input.split("\n\n"))
