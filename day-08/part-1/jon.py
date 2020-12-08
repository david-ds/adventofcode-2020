from tool.runners.python import SubmissionPy


class JonSubmission(SubmissionPy):

    def run(self, s):
        code = s.strip().split("\n")

        pc = 0
        acc = 0
        executed = set()

        while True:
            if pc in executed:
                return acc
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
                raise Exception("Invalid instruction {} at pc={}".format(instr, pc))
