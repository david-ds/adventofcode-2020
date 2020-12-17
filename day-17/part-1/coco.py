from tool.runners.python import SubmissionPy
import numpy as np
import scipy
from scipy.signal import convolve
from typing import List

def pretty_print(grid):
    for z in range(grid.shape[2]):
        print("z=", z)
        print(grid[:, :, z].astype("float"))

class CocoSubmission(SubmissionPy):

    def run(self, s, n_cycles=6):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        grid = s.split("\n")
        
        #### Fill grid
        total_size_grid = len(grid) + n_cycles*2 + 2 # PADDING
        full_grid = np.full((total_size_grid, total_size_grid, total_size_grid), fill_value=False)
        start_point_x_y = (len(full_grid) - len(grid)) // 2
        start_point_z = len(full_grid)// 2
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "#":
                    full_grid[start_point_x_y+i, start_point_x_y+j, start_point_z] = True

        # CONVOLUTIONS
        # this filter returns the number of active cubes around a cube
        filter_number_around = np.ones((3, 3, 3))
        filter_number_around[1, 1, 1] = 0

        for _ in range(n_cycles):
            number_around = convolve(full_grid, filter_number_around, mode="same", method="direct")
            number_around_2 = (number_around == 2)
            number_around_3 = (number_around == 3)
            active_1 = full_grid & (number_around_2 | number_around_3)  # those are the cubes that remain active
            active_2 = (~ full_grid) & number_around_3
            full_grid = active_1 | active_2
        return full_grid.sum()
