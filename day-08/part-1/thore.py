from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        program = s.splitlines()
        pc = 0
        acc = 0

        pc_values = set()

        while pc not in pc_values:
            instruction = program[pc]
            op, arg = instruction.split(" ")
            pc_values.add(pc)

            if op == "acc":
                acc += int(arg)
                pc += 1
            elif op == "jmp":
                pc += int(arg)
            elif op == "nop":
                pc += 1
            else:
                raise ValueError(f"Unknown operation: {op}")

        return acc
