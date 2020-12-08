from collections import deque

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
            if operation == "jmp" or operation == "nop":
                instructions[i] = (operation, i + int(arg))
            else:
                instructions[i] = (operation, int(arg))

        def swap(i):
            operation, arg = instructions[i]
            instructions[i] = ("jmp" if operation == "nop" else "nop", arg)

        seen = set()
        changes_to_try = deque()
        not_working = set()
        current_swap = None
        i = 0
        while i < len(instructions):
            if i in seen:
                # try to swap an instruction
                if current_swap is not None:
                    not_working.add(current_swap)
                    swap(current_swap)  # revert swap

                current_swap, seen_at_that_time = changes_to_try.pop()
                swap(current_swap)  # do the swap
                i = current_swap  # start from that instruction
                seen = seen_at_that_time
                continue

            operation, arg = instructions[i]
            change_to_try = (i, seen.copy())
            seen.add(i)
            if operation == "jmp":
                if i not in not_working:
                    changes_to_try.appendleft(change_to_try)
                i = arg
            elif operation == "nop":
                if i not in not_working:
                    changes_to_try.appendleft(change_to_try)
                i += 1
            else:
                i += 1

        # Correct swap has been found, we are able to terminate -> we can compute the accumulator
        acc = 0
        i = 0
        while i < len(instructions):
            operation, arg = instructions[i]
            if operation == "acc":
                acc += arg
                i += 1
            elif operation == "jmp":
                i = arg
            else:
                i += 1

        return acc
