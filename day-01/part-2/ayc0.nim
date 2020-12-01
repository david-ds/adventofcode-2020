import os, times
import strutils
from sequtils import map

proc run(s: string): string =
    var array = s.split("\n").map(parseInt)

    var i = 0
    var j = 0
    var k = 0
    var n = array.len

    var x: int
    var y: int
    var z: int

    while i < n:
        x = array[i]
        j = i + 1
        while j < n:
            y = array[j]
            if x + y > 2020:
                inc(j)
                continue
            k = j + 1
            while k < n:
                z = array[k]
                if x + y + z == 2020:
                    return $(x * y * z)
                inc(k)
            inc(j)
        inc(i)

    return ""


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
