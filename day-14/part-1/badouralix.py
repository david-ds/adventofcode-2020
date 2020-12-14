from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        mask0 = 0
        mask1 = 0
        mem = dict()

        for line in s.split("\n"):
            if line.startswith("mask"):
                data = line[6:]
                mask0 = int(data.replace("X", "1"), 2)
                mask1 = int(data.replace("X", "0"), 2)
            elif line.startswith("mem"):
                rawaddress, rawdata = line.split(" = ")
                address = int(rawaddress[4:-1])
                data = int(rawdata)
                override = (data | mask1) & mask0
                mem[address] = override

        return sum(mem[address] for address in mem)
