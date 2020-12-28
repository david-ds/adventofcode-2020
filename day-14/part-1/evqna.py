from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):
    def run(self, s):
        instructions = s.splitlines()

        mem = {}
        mask_0, mask_1 = 0, 0
        for ins in instructions:
            op, val = ins.split(' = ')
            if op.startswith('mem'):
                addr = int(op[4:-1])
                mem[addr] = (int(val) | mask_0) & mask_1
            elif op.startswith('mask'):
                mask_0 = int(val.replace('X', '0'), 2)
                mask_1 = int(val.replace('X', '1'), 2)
        return sum(mem.values())
