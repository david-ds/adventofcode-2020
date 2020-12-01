import os, times

proc run(s: string): string =
    # Your code here
    return s


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
