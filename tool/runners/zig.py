import errno
import subprocess
import tempfile

from tool.runners.wrapper import SubmissionWrapper


class SubmissionZig(SubmissionWrapper):
    def __init__(self, file):
        SubmissionWrapper.__init__(self)
        tmp = tempfile.NamedTemporaryFile(prefix="aoc")
        tmp.close()
        compile_output = subprocess.check_output(
            ["zig", "build-exe", "-OReleaseFast", "--strip", "-lc", "-femit-bin=" + tmp.name, file]
        ).decode()
        if compile_output:
            raise CompilationError(compile_output)
        self.executable = tmp.name

    def language(self):
        return "zig"

    def exec(self, input):
        try:
            return subprocess.check_output([self.executable, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                return CompilationError(e)
            else:
                # subprocess exited with another error
                return RuntimeError(e)