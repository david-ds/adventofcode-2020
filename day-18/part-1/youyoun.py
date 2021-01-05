from tool.runners.python import SubmissionPy
from queue import LifoQueue

ops = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b, '/': lambda a, b: a / b}


def evaluate(q):
    a, b, op = None, None, None
    while q.qsize() > 0:
        c = q.get()
        if c == '(':
            tmp_q = LifoQueue()
            tmp = [c]
            n_open_par = 1
            while n_open_par != 0:
                c = q.get()
                if c == '(':
                    n_open_par += 1
                elif c == ')':
                    n_open_par -= 1
                tmp.append(c)
            [tmp_q.put(x) for x in tmp[-2:0:-1]]
            c = evaluate(tmp_q)

        if c not in ops:
            if a is None:
                a = int(c)
            else:
                b = int(c)
        else:
            op = c
        if None not in {a, b, op}:
            res = ops[op](a, b)
            if q.empty():
                return res
            q.put(res)
            a, b, op = None, None, None


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        sum_ = 0
        for eq in s.replace(' ', '').splitlines():
            eq_q = LifoQueue()
            for c in eq[::-1]:
                eq_q.put(c)
            sum_ += evaluate(eq_q)
        return sum_


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
