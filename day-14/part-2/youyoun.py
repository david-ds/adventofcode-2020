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
                addr = to_bin(addr)
                num = list(mask)
                n_floating = 0
                for i, c in enumerate(num):
                    if c == '0':
                        num[i] = addr[i]
                    elif c == 'X':
                        num[i] = '{}'
                        n_floating += 1
                num = ''.join(num)
                for i in range(2 ** n_floating):
                    xs = f'{bin(i)[2:]:>0{n_floating}}'
                    new_addr = num.format(*list(xs))
                    mem[int(new_addr, 2)] = val
        return sum(mem.values())


def to_bin(int_):
    return f"{bin(int_)[2:]:>036}"


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
