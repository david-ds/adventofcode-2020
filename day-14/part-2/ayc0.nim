from times import cpuTime
from os import paramStr
import strutils
import bitops
import tables

var mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
var memory = newTable[uint64, uint64]()
var allOnes = 0b1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111_1111'u64

proc run(s: string): uint64 =
    var lines = splitLines(strip(s))

    for line in lines:
        if line[1] == 'a':
            # mask = "<>"
            mask = line[7 .. line.len - 1]
            # echo mask
            continue

        # mem[<entry>] = <value>
        var indexOfEndBracket = line.find(']')
        if indexOfEndBracket == -1:
            continue
        # to catch the values in "mem[<entry>] = <value>
        var entry: uint64 = uint64(parseUInt(line[4 .. indexOfEndBracket - 1]))
        var value: uint64 = uint64(parseUInt(line[indexOfEndBracket + 4 .. line.len - 1]))
        # echo entry, "<-", value

        var correctedEntry = entry
        var floatings = newSeq[uint8]()

        # 36 is the length of the mask
        var thisMask = ' ';
        for i in 0 .. 35:
            thisMask = mask[35 - i]
            if thisMask == '0':
                continue
            elif thisMask == '1':
                correctedEntry.setMask(rotateLeftBits(uint64(1), i))
            else:
                floatings.add(uint8(i))

        # echo floatings

        var correctedEntries = @[correctedEntry]
        var tmpCorrectedEntries = newSeq[uint64]()
        for floating in floatings:
            for correctedEntry in correctedEntries:
                # marked bit at floating to 0
                tmpCorrectedEntries.add(correctedEntry.masked(allOnes - rotateLeftBits(uint64(1), floating)))
                # marked bit at floating to 1
                tmpCorrectedEntries.add(correctedEntry.setMasked(rotateLeftBits(uint64(1), floating)))
            correctedEntries = tmpCorrectedEntries
            tmpCorrectedEntries = @[]

        # echo correctedEntries
        for correctedEntry in correctedEntries:
            memory[correctedEntry] = value

    var total: uint64 = 0
    for value in memory.values:
        total += value

    return total


var input: string = paramStr(1)
# var input = """
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# """

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
