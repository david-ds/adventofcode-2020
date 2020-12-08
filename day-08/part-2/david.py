from tool.runners.python import SubmissionPy

class InfiniteLoop(Exception):
    pass

class DavidSubmission(SubmissionPy):
    def run_program(self, program):
        acc, pos, finish_pos, visited = 0, 0, len(program), set()
        while pos != finish_pos:
            if pos in visited:
                # infinite loop
                raise InfiniteLoop()
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

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        lines = s.split("\n")
        program = [None]*len(lines)
        for idx, line in enumerate(lines):
            op = line[:3]
            arg = int(line[4:])
            program[idx] = (op, arg)
        
        for idx, instruction in enumerate(program):
            op, arg = instruction
            if op == "acc":
                continue
            
            if op == "jmp":
                program[idx] = ("nop", arg)
            else:
                program[idx] = ("jmp", arg)
            
            try:
                return self.run_program(program)
            except InfiniteLoop:
                # reset the instruction
                program[idx] = (op, arg)
