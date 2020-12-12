import errno
import tempfile
import subprocess

from tool.runners.exceptions import CompilationError
from tool.runners.wrapper import SubmissionWrapper


class SubmissionNim(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        tmp = tempfile.NamedTemporaryFile(prefix="aoc")
        tmp.close()
        compile_output = subprocess.check_output(
            [
                "nim",
                "compile",
                "--hints:off",  # no log during compilation
                "-d:release",  # optimized build
                "--opt:speed",  # optimized for speed
                "--checks:off",  # no runtime check
                "-o:" + tmp.name,
                file,
            ]
        ).decode()
        if compile_output:
            raise CompilationError(compile_output)
        self.executable = tmp.name

    def language(self):
        return "nim"

    def exec(self, input):
        try:
            return subprocess.check_output([self.executable, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return None
            else:
                # subprocess exited with another error
                return None
