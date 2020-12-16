import os
import sys

from Cython.Build import cythonize
from distutils.core import setup


CYTHON_DEBUG = bool(os.getenv("CYTHON_DEBUG", ""))

os.environ["CFLAGS"] = os.environ.get("CFLAGS", "") + " -O3"

build_dir = sys.argv.pop()
script_name = sys.argv.pop()

included = set()
include_dirs = []
with open(script_name, "r") as script:
    for line in script.readlines():
        if line.startswith("cimport numpy") and "numpy" not in included:
            import numpy
            include_dirs.append(numpy.get_include())
            included.add("numpy")

setup(
    ext_modules=cythonize(
        script_name,
        build_dir=build_dir,
        quiet=not CYTHON_DEBUG,
        annotate=CYTHON_DEBUG,
        compiler_directives={"language_level": 3},
    ),
    include_dirs=include_dirs,
)
