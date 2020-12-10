from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = []
        accumulator = 0
        visited = set()
        for line in s.split('\n'):
            splitted = line.split(' ')
            instruction = splitted[0]
            value = int(splitted[1])
            instructions.append((instruction, value))
        i = 0
        while i < len(instructions):
            command = instructions[i]
            if i in visited:
                return accumulator
            visited.add(i)
            if command[0] == "nop":
                pass
            elif command[0] == "acc":
                accumulator += command[1]
            elif command[0] == "jmp":
                i += command[1]
                continue
            i += 1
