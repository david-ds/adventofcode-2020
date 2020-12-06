from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        valid = 0
        for line in input.split("\n"):
            policy, letter_with_colon, password = line.split(" ")
            policy_min, policy_max = policy.split("-")
            letter = letter_with_colon[:-1]
            actual_count = password.count(letter)
            if int(policy_min) <= actual_count <= int(policy_max):
                valid += 1

        return valid
