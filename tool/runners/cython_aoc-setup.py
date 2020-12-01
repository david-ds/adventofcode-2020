import os
import sys

from Cython.Build import cythonize
from distutils.core import setup


CYTHON_DEBUG = bool(os.getenv("CYTHON_DEBUG", ""))

build_dir = sys.argv.pop()
script_name = sys.argv.pop()

setup(
    ext_modules=cythonize(
        script_name,
        build_dir=build_dir,
        quiet=not CYTHON_DEBUG,
        annotate=CYTHON_DEBUG,
        compiler_directives={"language_level": 3},
    )
)
