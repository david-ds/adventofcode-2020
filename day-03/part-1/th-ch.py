from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        nb_trees = 0
        x = 0
        y = 0
        lines = input.split("\n")
        for line in lines[:-1]:
            x += 3
            y += 1
            if lines[y][x % len(lines[y])] == "#":
                nb_trees += 1
        return nb_trees
