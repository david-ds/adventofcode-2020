from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        program = self.parse_program(s)
        for i, (op, arg) in enumerate(program):
            if op == "jmp":
                program[i] = ("nop", arg)
            elif op == "nop":
                program[i] = ("jmp", arg)
            else:
                continue

            acc = self.run_program(program)
            if acc is not None:
                return acc

            program[i] = (op, arg)

    @classmethod
    def parse_program(cls, s):
        return [cls.parse_instruction(line) for line in s.splitlines()]

    @staticmethod
    def parse_instruction(instruction):
        op, arg = instruction.split()
        arg = int(arg)
        return op, arg

    @staticmethod
    def run_program(program):
        pc = 0
        acc = 0
        visited = set()

        while pc != len(program):
            if pc in visited:
                return None  # infinite loop
            visited.add(pc)

            op, arg = program[pc]

            if op == "acc":
                acc += arg
                pc += 1
            elif op == "jmp":
                pc += arg
            elif op == "nop":
                pc += 1
            else:
                raise ValueError(f"Unknown operation: {op}")

        return acc
