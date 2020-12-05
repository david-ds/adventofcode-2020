from times import cpuTime
from os import paramStr

proc run(s: string): string =
    # Your code here
    return ""


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
