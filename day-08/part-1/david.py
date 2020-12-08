from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        program = []
        for line in s.split("\n"):
            op = line[:3]
            arg = int(line[4:])
            program.append((op, arg))

        acc, pos, visited = 0, 0, set()
        while True:
            if pos in visited:
                return acc
            visited.add(pos)
            op, param = program[pos]
            if op == "nop":
                pos += 1
            elif op == "jmp":
                pos += param
            elif op == "acc":          
                acc += param
                pos += 1

        return acc

