from times import cpuTime
from os import paramStr
import strutils

type Bus = object
    base: int
    offset: int


proc run(s: string): int =
    var lines = s.split('\n')
    var rawBusIDs = lines[1].split(',')
    var buses: seq[Bus]
    var offset = 0

    var prodCumulated = 1

    for busID in rawBusIDs:
        if busID == "x":
            offset += 1
            continue
        var base = parseInt(busID)
        prodCumulated *= base
        buses.add(Bus(base: base, offset: offset))
        offset += 1

    buses.del(0)
    # echo buses

    var total = 0

    for bus in buses:
        var ni = prodCumulated div bus.base
        var vi = 1
        while ((vi * ni) mod bus.base) != 1:
            vi += 1
        total += ((vi * ni) * -bus.offset)

    return (total mod prodCumulated) + prodCumulated



var input: string = paramStr(1)
# var input = """939
# 7,13,x,x,59,x,31,19
# """

var t0 = cpuTime()
var output = run(input)


echo "_duration:", (cpuTime() - t0) * 1000
echo output
