from tool.runners.python import SubmissionPy

from collections import defaultdict
from itertools import product


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        mem = dict()

        for line in s.split("\n"):
            if line.startswith("mask"):
                mask = defaultdict(list)
                for i, c in enumerate(line[7:]):
                    mask[c].append(i)
            elif line.startswith("mem"):
                rawaddress, rawdata = line.split(" = ")
                address = f"{int(rawaddress[4:-1]):036b}"
                data = int(rawdata)

                # Pray for the very first line to start with a mask
                override = list(address)
                for i in mask["1"]:
                    override[i] = "1"
                for i in mask["X"]:
                    override[i] = "X"

                for patch in product(["0", "1"], repeat=len(mask["X"])):
                    for i, p in enumerate(patch):
                        override[mask["X"][i]] = p
                    mem["".join(override)] = data

        return sum(mem[address] for address in mem)
