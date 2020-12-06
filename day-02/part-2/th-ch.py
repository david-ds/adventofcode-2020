from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        valid = 0
        for line in input.split("\n"):
            policy, letter_with_colon, password = line.split(" ")
            first, second = policy.split("-")
            letter = letter_with_colon[:-1]
            if (password[int(first) - 1] == letter) != (
                password[int(second) - 1] == letter
            ):
                valid += 1

        return valid
