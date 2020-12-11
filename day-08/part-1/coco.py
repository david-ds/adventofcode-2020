from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):


    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        instructions = [instr.split() for instr in s.strip().split("\n")]

        acc = 0
        pointer = 0
        visited_positions = set()
        while True:
            instr, value = instructions[pointer]
            if instr == "acc":
                acc += int(value)
                pointer += 1
            elif instr == "jmp":
                pointer += int(value)
            else:
                pointer += 1

            if pointer in visited_positions:
                break
            visited_positions.add(pointer)

        return acc
