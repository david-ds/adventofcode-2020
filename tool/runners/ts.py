import errno
import subprocess

from tool.runners.wrapper import SubmissionWrapper


class SubmissionTs(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        self.file = file

    def language(self):
        return "ts"

    def exec(self, input):
        try:
            return subprocess.check_output(["./node_modules/.bin/ts-node", self.file, input]).decode()
        except OSError as e:
            raise RuntimeError(e)

    def __call__(self):
        return SubmissionTs(self.file)
