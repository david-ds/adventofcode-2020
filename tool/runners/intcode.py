import collections


class SubmissionIntcode:

    def __init__(self, file):
        with open(file, "r") as f:
            code_str = f.read()
        self.code = [int(v) for v in code_str.strip().split(",")]

    def language(self):
        return "intcode"

    def run(self, input):
        inputs = [int(v) for v in input.strip().split(",")]
        out = compute(self.code, [len(inputs)] + inputs)
        return ",".join(str(v) for v in out)

    def cleanup(self):
        pass


def compute(code, inputs):
    p = collections.defaultdict(int, enumerate(code))
    pc = 0
    relative_base = 0

    def index(pos):
        mode = (p[pc] // 10 ** (1 + pos)) % 10
        if mode == 0:
            return p[pc + pos]
        if mode == 1:
            return pc + pos
        if mode == 2:
            return relative_base + p[pc + pos]
        raise Exception("Bad param mode")

    input_index = 0

    while True:
        op = p[pc] % 100

        if op == 1:
            p[index(3)] = p[index(1)] + p[index(2)]
            pc += 4
        elif op == 2:
            p[index(3)] = p[index(1)] * p[index(2)]
            pc += 4
        elif op == 3:
            p[index(1)] = inputs[input_index]
            input_index += 1
            pc += 2
        elif op == 4:
            yield p[index(1)]
            pc += 2
        elif op == 5:
            pc = p[index(2)] if p[index(1)] != 0 else pc + 3
        elif op == 6:
            pc = p[index(2)] if p[index(1)] == 0 else pc + 3
        elif op == 7:
            p[index(3)] = 1 if p[index(1)] < p[index(2)] else 0
            pc += 4
        elif op == 8:
            p[index(3)] = 1 if p[index(1)] == p[index(2)] else 0
            pc += 4
        elif op == 9:
            relative_base += p[index(1)]
            pc += 2
        elif op == 99:
            break
        else:
            raise Exception("Unknown op code")
