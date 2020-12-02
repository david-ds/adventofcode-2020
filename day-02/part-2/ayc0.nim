import os, times
import strutils
from sequtils import map

proc matches(line: string): bool =
    var parts = line.split(" ")
    var indexes = parts[0].split("-").map(parseInt)
    var password = parts[1][0]
    var word = parts[2]
    var x = word[indexes[0] - 1]
    var y = word[indexes[1] - 1]
    return x != y and (x == password or y == password)

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
