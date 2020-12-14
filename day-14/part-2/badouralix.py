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
                maskedaddress = ""
                for i in range(len(address)):
                    if mask[i] == "0":
                        maskedaddress += address[i]
                    else:
                        maskedaddress += mask[i]

                # Assume there is at least one X
                for patch in product(["0", "1"], repeat=len(xindices)):
                    override = maskedaddress[: xindices[0]]

                    for i, p in enumerate(patch):
                        override += p

                        if i == len(patch) - 1:
                            override += "".join(maskedaddress[xindices[i] + 1 :])
                        else:
                            override += "".join(
                                maskedaddress[xindices[i] + 1 : xindices[i + 1]]
                            )
                    mem[override] = data

        return sum(mem[address] for address in mem)
