from tool.runners.python import SubmissionPy
import re
from itertools import product


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
        indexes_X = []

        for line in lines:
            if line.startswith("mask"):
                mask: str = line[7:]
                indexes_X = list(reversed([i for i in range(len(mask)) if mask[i] == "X"]))
                mask_0 = int(mask.replace("X", "0"), 2)
            else:
                m = re.match(regex_value, line)
                address, value = m.groups()
                address, value = int(address), int(value)
                address = address | mask_0  # set all required values to 1
                address_bits = list((f"{address:036b}"))  #list(bin(address)[2:])

                for prod in product(["0", "1"], repeat=len(indexes_X)):
                    for k, bit_value in zip(indexes_X, prod):
                        address_bits[k] = bit_value
                    address = int("".join(address_bits), 2)
                    memory[address] = value

        return sum(val for val in memory.values())
