from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        program = [(line[:3], int(line[4:])) for line in s.split("\n")]

        for ip in range(len(program)):
            patched = self.patch(program, ip)
            if not patched:
                continue

            accumulator, finished = self.execute(program)
            if not finished:
                self.patch(program, ip)
                continue

            return accumulator

    def patch(self, program, ip):
        operation, argument = program[ip]

        if operation == "jmp":
            program[ip] = ("nop", argument)
            return True
        elif operation == "nop":
            program[ip] = ("jmp", argument)
            return True

        return False

    def execute(self, program):
        accumulator = 0
        ip = 0
        size = len(program)
        visited = set()

        while ip not in visited and ip < size:
            visited.add(ip)
            operation, argument = program[ip]

            if operation == "acc":
                accumulator += argument
                ip += 1
            elif operation == "jmp":
                ip += argument
            elif operation == "nop":
                ip += 1
            else:
                raise Exception(f"Operation {operation} at {ip} is not implemented")

        return accumulator, (ip == size)
