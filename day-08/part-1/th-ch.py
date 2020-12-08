from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = {}
        for i, instruction in enumerate(s.split("\n")):
            operation, arg = instruction.split(" ")
            if operation == "jmp":
                instructions[i] = (operation, i + int(arg))
            else:
                instructions[i] = (operation, int(arg))

        acc = 0
        seen = set()
        i = 0
        while i not in seen:
            operation, arg = instructions[i]
            seen.add(i)
            if operation == "acc":
                acc += arg
                i += 1
            elif operation == "jmp":
                i = arg
            else:
                i += 1

        return acc
