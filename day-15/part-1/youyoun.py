from tool.runners.python import SubmissionPy
from collections import defaultdict


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        mem = defaultdict(list)
        turn = 1
        init = s.splitlines()[0].split(',')
        while turn <= len(init):
            last_spoken = int(init[turn - 1])
            mem[last_spoken].append(turn)
            turn += 1
        while turn < 2021:
            if len(mem[last_spoken]) >= 2:
                last_spoken = mem[last_spoken][-1] - mem[last_spoken][-2]
            else:
                last_spoken = 0
            mem[last_spoken].append(turn)
            turn += 1
        return last_spoken


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
