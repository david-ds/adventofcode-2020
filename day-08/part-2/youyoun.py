from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = s.splitlines()
        i = 0
        acc = 0
        while True:
            instr = instructions[i]
            op, arg = instr.split(' ')
            arg = int(arg)
            if op == 'acc':
                acc += arg
                i += 1
            elif op == 'jmp':
                swap_acc = run(instructions[:i] + [instructions[i].replace('jmp', 'nop')] + instructions[i + 1:], i)
                if swap_acc == -1:
                    i += arg
                else:
                    return acc + swap_acc
            elif op == 'nop':
                swap_acc = run(instructions[:i] + [instructions[i].replace('nop', 'jmp')] + instructions[i + 1:], i)
                if swap_acc == -1:
                    i += 1
                else:
                    return acc + swap_acc


def run(instructions, i):
    acc = 0
    run_instr = set()
    while i not in run_instr:
        run_instr.add(i)
        op, arg = instructions[i].split(' ')
        arg = int(arg)
        if op == 'acc':
            acc += arg
            i += 1
        elif op == 'jmp':
            i += arg
        elif op == 'nop':
            i += 1
        if i >= len(instructions):
            return acc
    return -1
