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
                xindices = [i for i, c in enumerate(mask) if c == "X"]
            elif line.startswith("mem"):
                rawaddress, rawdata = line.split(" = ")
                address = f"{int(rawaddress[4:-1]):036b}"
                data = int(rawdata)

                # Pray for the very first line to start with a mask
                assert len(address) == len(mask)
                override = list()
                for i in range(len(address)):
                    if mask[i] == "0":
                        override.append(address[i])
                    else:
                        override.append(mask[i])

                for patch in product(["0", "1"], repeat=len(xindices)):
                    for i, p in enumerate(patch):
                        override[xindices[i]] = p
                    mem["".join(override)] = data

        return sum(mem[address] for address in mem)
