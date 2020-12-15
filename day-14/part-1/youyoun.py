from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        mem = {}
        mask = []
        for e in s:
            if e.startswith('mask'):
                mask = e.split(' = ')[1].strip()
            else:
                parsed = e.split(' = ')
                addr, val = int(parsed[0][4:-1]), int(parsed[1])
                val = to_bin(val)
                num = list(mask)
                for i, c in enumerate(num):
                    if c == 'X':
                        num[i] = val[i]
                mem[addr] = int(''.join(num), 2)
        return sum(mem.values())


def to_bin(int_):
    return f"{bin(int_)[2:]:>036}"


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
