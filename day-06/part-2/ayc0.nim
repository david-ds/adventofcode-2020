from times import cpuTime
from os import paramStr
from bitops import rotateLeftBits, rotateRightBits, bitor, bitand

var base = uint32('a')

proc reduce(map: uint32): uint32 =
    var acc = map
    var count = 0b0'u32
    for i in 0..25:
        count = count + (acc and 0b1'u32)
        acc = rotateRightBits(acc, 1)
    return count

proc run(s: string): string =
    var previousLetter = '\n'
    var total = 0b0'u32
    var groupTotal = 0b111111111111111111111111111111'u32
    var personTotal = 0b0'u32
    var skip = true
    for letter in s & "\n\n":
        if letter == '\n':
            if previousLetter == '\n':
                if skip:
                    continue
                total = total + reduce(groupTotal)
                groupTotal = 0b111111111111111111111111111111'u32
                skip = true
            else:
                groupTotal = groupTotal and personTotal
            skip = false
            previousLetter = letter
            personTotal = 0b0'u32
            continue
        personTotal = personTotal or rotateLeftBits(0b1'u32, uint32(letter) - base)
        previousLetter = letter
    return $total

var t0 = cpuTime()
var input: string = paramStr(1)
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
