from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = s.strip().split("\n")

        pc = 0
        acc = 0
        executed = set()

        while True:
            executed.add(pc)

            instr, val = code[pc].split(" ")

            if instr == "acc":
                acc += int(val)
                pc += 1
            elif instr == "jmp":
                # Try as a "nop"
                t = try_terminate(code, pc + 1, executed, acc)  # No executed.copy() here, on purpose
                if t is not None:
                    return t
                # Continue as a "jmp"
                pc += int(val)
            elif instr == "nop":
                # Try as a "jmp"
                t = try_terminate(code, pc + int(val), executed, acc)
                if t is not None:
                    return t
                # Continue as a "nop"
                pc += 1
            else:
                raise Exception("invalid")


def try_terminate(code, pc, executed, acc):
    n = len(code)
    while True:
        if pc == n:
            return acc
        elif pc in executed:
            return None  # loop or path that was already tried
        executed.add(pc)

        instr, val = code[pc].split(" ")
        if instr == "acc":
            acc += int(val)
            pc += 1
        elif instr == "jmp":
            pc += int(val)
        elif instr == "nop":
            pc += 1
        else:
            raise Exception("invalid")
