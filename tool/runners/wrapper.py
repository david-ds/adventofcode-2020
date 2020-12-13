"""
Wrapper class handling the communication between the main python process and
the funky language subprocesses.
"""

from tool.runners.python import SubmissionPy


class SubmissionWrapper(SubmissionPy):
    def __init__(self):
        SubmissionPy.__init__(self)

    # Method that every class implementing SubmssionWrapper should override
    def exec(self, input):
        pass

    def run(self, input):
        stdout = self.exec(input)
        lines = stdout.split("\n")[:-1]

        duration_line = None
        for line in lines:
            if line.startswith("_duration:"):
                duration_line = line
                break
        lines = [line for line in lines if not line.startswith("_duration:")]

        if len(lines) == 0:
            return None, duration_line, []

        return lines[-1], duration_line, lines[:-1]
