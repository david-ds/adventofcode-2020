from tool.runners.python import SubmissionPy

import math

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.split("\n")
        self.buses = [(int(idx),int(val)) for idx,val in enumerate(lines[1].split(",")) if val != "x"]

        current_idx = 0
        jump = 1
        t = 0
        while True:
            bus_id, bus_val = self.buses[current_idx]
            if (t + bus_id) % bus_val == 0:
                jump *= bus_val
                current_idx += 1
            
            if current_idx == len(self.buses):
                return t

            t += jump
