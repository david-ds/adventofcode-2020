from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        program = [(line[:3], int(line[4:])) for line in s.split("\n")]

        accumulator = 0
        ip = 0
        visited = set()

        while ip not in visited:
            visited.add(ip)
            accumulator, ip = self.step(program, accumulator, ip)

        return accumulator

    def step(self, program, accumulator, ip):
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

        return accumulator, ip
