from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    slope = (3, 1)

    def run(self, s):
        grid = s.splitlines()
        W, H = len(grid[0]), len(grid)
        n_trees = 0
        x, y = 0, 0
        while y < H:
            if grid[y][x] == '#':
                n_trees += 1
            x = (x + self.slope[0]) % W
            y += self.slope[1]
        return n_trees
