import errno
import subprocess

from tool.runners.wrapper import SubmissionWrapper


class SubmissionDenoTS(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        self.file = file

    def language(self):
        return "deno.ts"

    def exec(self, input):
        try:
            return subprocess.check_output(["deno", self.file, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return None
            else:
                # subprocess exited with another error
                return None

    def __call__(self):
        return SubmissionDenoTS(self.file)
