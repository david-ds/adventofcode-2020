from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        lines = input.split("\n")
        result = 1
        policies = [
            lambda x, y: (x + 1, y + 1),
            lambda x, y: (x + 3, y + 1),
            lambda x, y: (x + 5, y + 1),
            lambda x, y: (x + 7, y + 1),
            lambda x, y: (x + 1, y + 2),
        ]
        for policy in policies:
            nb_trees = 0
            x = 0
            y = 0
            while y < len(lines):
                if lines[y][x % len(lines[y])] == "#":
                    nb_trees += 1
                x, y = policy(x, y)
            result *= nb_trees

        return result
