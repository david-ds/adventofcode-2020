import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        mem = {}
        prog = re.compile(r"mem\[(\d+)\] = (\d+)")
        self.x_prog = re.compile(r"X")
        for line in s.splitlines():
            if line.startswith("mask"):
                mask = line.split(" = ")[1]
            elif (m := prog.match(line)) :
                key, value = m.groups()
                value = int(value)
                key_bin = format(int(key), f"0{len(mask)}b")
                key_masked = "".join(
                    m if m in ["1", "X"] else c for c, m in zip(key_bin, mask)
                )
                for address in self.generate_adresses(key_masked):
                    mem[address] = value
        return sum(mem.values())

    def generate_adresses(self, key_masked):
        x_count = key_masked.count("X")
        for i in range(2 ** x_count):
            it = iter(format(i, f"0{x_count}b"))
            yield self.x_prog.sub(lambda m: next(it), key_masked)


def test_day14_part1():
    assert (
        ThoreSubmission().run(
            """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
        )
        == 208
    )
