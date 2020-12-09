from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        acc = 0
        instructions = s.splitlines()
        run_instr = set()
        i = 0
        while True:
            if i in run_instr:
                break
            run_instr.add(i)
            instr = instructions[i]
            op, arg = instr.split(' ')
            arg = int(arg)
            if op == 'acc':
                acc += arg
            elif op == 'jmp':
                i += arg
                continue
            elif op == 'nop':
                pass
            i += 1
        return acc
