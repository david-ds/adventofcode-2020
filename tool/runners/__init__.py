#!/usr/bin/env python3

# project
from tool.runners.bash import SubmissionBash
from tool.runners.c import SubmissionC
from tool.runners.cpp import SubmissionCpp
from tool.runners.go import SubmissionGo
from tool.runners.intcode import SubmissionIntcode
from tool.runners.java import SubmissionJava
from tool.runners.node import SubmissionNode
from tool.runners.deno import SubmissionDeno
from tool.runners.deno_ts import SubmissionDenoTS
from tool.runners.cython_aoc import SubmissionPyx
from tool.runners.python import SubmissionPy
from tool.runners.ruby import SubmissionRb
from tool.runners.rust import SubmissionRs
from tool.runners.ts import SubmissionTs
from tool.runners.wrapper import SubmissionWrapper
from tool.runners.julia import SubmissionJulia
from tool.runners.vlang import SubmissionV
from tool.utils import load_subclass

TOOL_BY_LANGUAGE = {
    "c": "gcc",
    "cpp": "g++",
    "go": "go",
    "intcode": "python",
    "java": "java",
    "js": "node",
    "deno.js": "deno",
    "deno.ts": "deno",
    "ts": "./node_modules/.bin/ts-node",
    "py": "python",
    "pyx": "cython",
    "rb": "ruby",
    "rs": "cargo",
    "sh": "bash",
    "jl": "julia",
    "v": "v"
}
LANGUAGES = list(TOOL_BY_LANGUAGE.keys())


def ext_by_language(x):
    return "." + str(x)


def load_submission_runnable(path, language):
    if language not in LANGUAGES:
        return None
    if language == "py":
        return load_subclass(path, SubmissionPy, exclude=[SubmissionWrapper])
    elif language == "pyx":
        return SubmissionPyx(path)
    elif language == "c":
        return SubmissionC(path)
    elif language == "cpp":
        return SubmissionCpp(path)
    elif language == "go":
        return SubmissionGo(path)
    elif language == "intcode":
        return SubmissionIntcode(path)
    elif language == "java":
        return SubmissionJava(path)
    elif language == "js":
        return SubmissionNode(path)
    elif language == "deno.js":
        return SubmissionDeno(path)
    elif language == "deno.ts":
        return SubmissionDenoTS(path)
    elif language == "rb":
        return SubmissionRb(path)
    elif language == "rs":
        return SubmissionRs(path)
    elif language == "sh":
        return SubmissionBash(path)
    elif language == "jl":
        return SubmissionJulia(path)
    elif language == "ts":
        return SubmissionTs(path)
    elif language == "v":
        return SubmissionV(path)
