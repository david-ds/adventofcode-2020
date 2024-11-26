from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        sum_ = 0
        for eq in s.replace('+', '**').replace(' ', '').splitlines():
            sum_ += eval(''.join([f'SpecialInt({x})' if x.isnumeric() else x for x in eq]))
        return sum_


class SpecialInt(int):
    def __pow__(self, power, modulo=None):
        return SpecialInt(int(self) + int(power))

    def __mul__(self, other):
        return SpecialInt(int(self) * int(other))


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
