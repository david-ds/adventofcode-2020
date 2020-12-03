from tool.runners.python import SubmissionPy

import math

class EvqnaSubmission(SubmissionPy):

    def trees_encountered(self, grid, w, h, slope):
        d_x, d_y = slope
        n_trees = 0
        x, y = 0, 0
        while y < h:
            if grid[y][x] == '#':
                n_trees += 1
            x = (x + d_x) % w
            y = y + d_y
        return n_trees        

    def run(self, s):
        slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]

        grid = s.splitlines()
        W, H = len(grid[0]), len(grid)

        trees = [self.trees_encountered(grid, W, H, s) for s in slopes]
        return math.prod(trees)
