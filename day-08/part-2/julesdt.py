from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def try_instructions(self, modified_index):
        accumulator = 0
        visited = set()
        i = 0
        while i < len(self.instructions):
            if i in visited:
                return None
            visited.add(i)
            if i == modified_index[0]:
                command = modified_index[1]
            else:
                command = self.instructions[i]
            if command[0] == "nop":
                pass
            elif command[0] == "acc":
                accumulator += command[1]
            elif command[0] == "jmp":
                i += command[1]
                continue
            i += 1
        return accumulator

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.instructions = []
        
        for line in s.split('\n'):
            splitted = line.split(' ')
            instruction = splitted[0]
            value = int(splitted[1])
            self.instructions.append((instruction, value))
        for i in range(len(self.instructions)):
            if self.instructions[i][0] == "nop":
                modified_value = "jmp"
            elif self.instructions[i][0] == "jmp":
                modified_value = "nop"
            else:
                continue
            value = self.try_instructions(modified_index=(i, modified_value))
            if value is not None:
                return value
