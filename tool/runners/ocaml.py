import errno
import os
import subprocess
import tempfile

from tool.runners.exceptions import CompilationError, RuntimeError
from tool.runners.wrapper import SubmissionWrapper


class SubmissionOCaml(SubmissionWrapper):
    
    file = None
    
    def __init__(self, file):
        DEVNULL = open(os.devnull, "wb")
        self.file = file
        SubmissionWrapper.__init__(self)
        dirname = os.path.dirname(file)
        exe = file.replace(".ml", ".exe")
        self.cleanup()
        with open(self.dune_path(), "w") as f:
            f.write(self.dune())
        try:
            subprocess.check_output(
            ["opam", "exec", "dune", "build"], stderr=DEVNULL
            ).decode()
        except subprocess.CalledProcessError as e:
            self.cleanup()
            raise CompilationError(e.output)
        self.cleanup()
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
    (libraries angstrom fmt str)
    (preprocess (pps ppx_deriving.std)))
        """
        return dune

    def language(self):
        return "ml"

    def exec(self, input):
        try:
            return subprocess.check_output([self.executable, input]).decode()
        except OSError as e:
            if e.errno == errno.ENOENT:
                # executable not found
                raise CompilationError(e)
            else:
                # subprocess exited with another error
                raise RuntimeError(e)
