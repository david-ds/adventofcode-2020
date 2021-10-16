from times import cpuTime
from os import paramStr
import strutils
import re
from sequtils import map

var commaXRegex = re"x(,|$)"

proc run(s: string): int =
    var lines = s.split('\n')
    var startingTimestamp = parseInt(lines[0])
    var currentTimestamp = startingTimestamp
    var busIDs = lines[1].replace(commaXRegex).split(',').map(parseInt)

    while true:
        for busID in busIDs:
            if currentTimestamp mod busID == 0:
                return busID * (currentTimestamp - startingTimestamp)
        currentTimestamp += 1

    return -1


var input: string = paramStr(1)
# var input = """939
# 7,13,x,x,59,x,31,19
# """

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
