from times import cpuTime
from os import paramStr
import strutils
import tables
import bitops

var mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
var memory = newTable[uint16, uint64]()

proc run(s: string): uint64 =
    var lines = splitLines(strip(s))
    # echo lines


    for line in lines:
        if line[1] == 'a':
            # mask = "<>"
            mask = line[7 .. line.len - 1]
            # echo mask
        else:
            # mem[<entry>] = <value>
            var indexOfEndBracket = line.find(']')
            if indexOfEndBracket == -1:
                continue
            # to catch the values in "mem[<entry>] = <value>
            var entry: uint16 = uint16(parseUInt(line[4 .. indexOfEndBracket - 1]))
            var value: uint64 = uint64(parseUInt(line[indexOfEndBracket + 4 .. line.len - 1]))
            # echo entry, "<-", value

            var finalValue: uint64 = 0

            # 36 is the length of the mask
            var thisMask = ' ';
            for i in 0 .. 35:
                thisMask = mask[35 - i]
                if thisMask == '0':
                    continue
                elif thisMask == '1':
                    finalValue += rotateLeftBits(uint64(1), i)
                else:
                    finalValue += value.masked(rotateLeftBits(uint64(1), i))

            memory[entry] = finalValue

    var total: uint64 = 0
    for value in memory.values:
        total += value

    return total


var input: string = paramStr(1)
# var input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# """

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
