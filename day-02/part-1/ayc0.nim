import os, times
import strutils
from sequtils import map

proc matches(line: string): bool =
    var parts = line.split(" ")
    var limits = parts[0].split("-").map(parseInt)
    var char_to_verify = parts[1][0]
    var word = parts[2]
    var i = 0
    for x in word:
        if x == char_to_verify:
            inc(i)
            if i > limits[1]:
                return false
    if i < limits[0]:
        return false
    return true

proc run(s: string): string =
    var lines = s.split("\n")
    var count = 0
    for line in lines:
        if matches(line):
            inc(count)
    return $count


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
