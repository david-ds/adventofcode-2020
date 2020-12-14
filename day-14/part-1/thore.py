import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        mem, mask_1, mask_0 = {}, 0, 0
        prog = re.compile(r"mem\[(\d+)\] = (\d+)")
        for line in s.splitlines():
            if line.startswith("mask"):
                mask = line.split(" = ")[1]
                mask_1 = int("".join(["1" if c == "1" else "0" for c in mask]), 2)
                mask_0 = int("".join(["0" if c == "0" else "1" for c in mask]), 2)
            elif (m := prog.match(line)) :
                key, value = m.groups()
                mem[key] = (int(value) | mask_1) & mask_0
        return sum(mem.values())


def test_day14_part1():
    assert (
        ThoreSubmission().run(
            """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
        )
        == 165
    )
