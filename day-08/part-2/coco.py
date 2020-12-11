from tool.runners.python import SubmissionPy
from collections import defaultdict

class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        # Your code goes here
        instructions = [instr.split() for instr in s.strip().split("\n")]

        parents = defaultdict(list)
        for i, (instr, value) in enumerate(instructions):
            if instr == "acc":
                parents[i + 1].append(i)
            elif instr == "jmp":
                parents[i + int(value)].append(i)
            else:
                parents[i + 1].append(i)

        # Contruct graph of items that can reach the last instruction
        will_reach_end = [False] * len(instructions)
        start = [len(instructions) - 1]  # last position
        already_visited = set()
        while start:
            p = start.pop()
            if p in already_visited:
                continue
            already_visited.add(p)
            will_reach_end[p] = True
            current_parents = parents[p]
            start.extend(current_parents)

        # Now, go along path, but if we can change one instruction
        # to reach the end, do it
        acc = 0
        pointer = 0
        already_changed = False
        while True:
            if pointer >= len(instructions):
                break
            instr, value = instructions[pointer]
            value = int(value)
            if instr == "acc":
                acc += value
                pointer += 1
            elif instr == "jmp":
                if not already_changed and will_reach_end[pointer + 1]:
                    # change to nop
                    pointer += 1
                    already_changed = True
                else:
                    pointer += value
            elif instr == "nop":
                if not already_changed and will_reach_end[pointer + value]:
                    # change to jmp
                    pointer += value
                    already_changed = True
                else:
                    pointer += 1
        return acc
