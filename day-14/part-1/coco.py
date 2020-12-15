from tool.runners.python import SubmissionPy
import re

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.split("\n")

        regex_value = re.compile(r"mem\[(\d*)\] = (\d*)")
        memory = dict()
        mask_0, mask_1 = 0, 0

        for line in lines:
            if line.startswith("mask"):
                mask = line[7:]
                # mask_and = value.replace("X", "1")
                mask_0 = int(mask.replace("X", "0"), 2)
                mask_1 = int(mask.replace("X", "1"), 2)
            else:
                m = re.match(regex_value, line)
                key, value = m.groups()
                key, value = int(key), int(value)
                value = mask_1 & value  # bitwise AND to set X values and correct zeros
                value = value | mask_0   # set correct ones
                memory[key] = value
            
        return sum(val for val in memory.values())

