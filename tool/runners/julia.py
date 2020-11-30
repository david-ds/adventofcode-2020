import errno
import subprocess

from tool.runners.wrapper import SubmissionWrapper


class SubmissionJulia(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        self.file = file

    def language(self):
        return "jl"

    def exec(self, input):
        try:
            return subprocess.check_output(["julia", self.file, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return None
            else:
                # subprocess exited with another error
                return None
        except subprocess.CalledProcessError as e:
            print(e.output.decode())

    def __call__(self):
        return SubmissionJulia(self.file)
