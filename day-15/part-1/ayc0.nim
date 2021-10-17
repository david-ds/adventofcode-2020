from times import cpuTime
from os import paramStr
from strutils import split, strip, parseUInt
from sequtils import map
import tables

type Cache = ref Table[uint, uint16]
var cache = new Cache


proc run(s: string): uint =
    var initNumbers = s.split(',').map(parseUInt)
    var turn = uint16(1)
    for initNumber in initNumbers:
        cache[initNumber] = turn
        inc(turn)

    var previousNumber = initNumbers[initNumbers.len - 1]
    var newNumber = previousNumber
    while turn <= 2020:
        var wasFoundAt = cache.getOrDefault(previousNumber, 0)
        if wasFoundAt == 0:
            # first time it was spoken
            newNumber = 0
        else:
            # it was spoken at least 2 times
            newNumber = turn - 1 - wasFoundAt

        # echo "New number: ", newNumber
        cache[previousNumber] = turn - 1
        previousNumber = newNumber

        inc(turn)

    return previousNumber


var input: string = strip(paramStr(1))
# input = "0,3,6"
# input = "1,3,2" # output should be 1
# input = "2,1,3" # output should be 10
# input = "3,1,2" # output should be 1836

# echo "\n\n=========\nSTART\n========="

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
