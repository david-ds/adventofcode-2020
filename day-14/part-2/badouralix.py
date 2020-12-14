from tool.runners.python import SubmissionPy

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
                mask = line[7:]
            elif line.startswith("mem"):
                rawaddress, rawdata = line.split(" = ")
                address = f"{int(rawaddress[4:-1]):036b}"
                data = int(rawdata)

                for patch in product(["0", "1"], repeat=mask.count("X")):
                    index = 0
                    override = ""

                    for i in range(36):
                        if mask[i] == "0":
                            override += address[i]
                        elif mask[i] == "1":
                            override += "1"
                        else:
                            override += patch[index]
                            index += 1

                    mem[override] = data

        return sum(mem[address] for address in mem)
