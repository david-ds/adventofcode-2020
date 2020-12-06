from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        return sum(
            len(
                set.intersection(
                    *[set(answer_by_person) for answer_by_person in answer.split("\n")]
                )
            )
            for answer in input.split("\n\n")
        )
