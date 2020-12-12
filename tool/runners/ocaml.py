import errno
import os
import subprocess

from tool.runners.exceptions import CompilationError, RuntimeError
from tool.runners.wrapper import SubmissionWrapper


class SubmissionOCaml(SubmissionWrapper):

    file = None

    def __init__(self, file):
        self.file = file
        SubmissionWrapper.__init__(self)
        exe = file.replace(".ml", ".exe")
        self.cleanup()
        with open(self.dune_path(), "w") as f:
            f.write(self.dune())
        output = subprocess.run(["esy"], capture_output=True)
        self.cleanup()
        if output.returncode != 0:
            raise CompilationError(output.stdout + output.stderr)
        self.executable = "_build/default/" + exe

    def cleanup(self):
        if os.path.exists(self.dune_path()):
            os.remove(self.dune_path())

    def dune_path(self):
        dirname = os.path.dirname(self.file)
        return dirname + "/dune"

    def dune(self):
        name = os.path.splitext(os.path.basename(self.file))[0]
        dune = f"""(executable
    (name {name})
    (libraries angstrom fmt str stdio)
    (ocamlopt_flags -O3)
    (preprocess (pps ppx_deriving.std)))
        """
        return dune

    def language(self):
        return "ml"

    def exec(self, input):
        try:
            p = subprocess.Popen(
                [self.executable, input],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = p.communicate(input.encode())
            if stderr.decode() != "":
                raise RuntimeError(stderr.decode())
            return stdout.decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                raise CompilationError(e)
            else:
                # subprocess exited with another error
                raise RuntimeError(e)
