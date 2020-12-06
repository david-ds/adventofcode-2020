from times import cpuTime
from os import paramStr
from strutils import split
from bitops import rotateLeftBits, rotateRightBits, bitand

type Seat = tuple
    row: uint8
    column: uint8

proc seatId(seat: Seat): uint16 =
    return rotateLeftBits(uint16(seat.row), 3) + uint16(seat.column)

proc analyze(boardingPass: string): Seat =
    if (boardingPass == ""):
        return (0b0'u8, 0b0'u8)

    var row = 0b0'u8
    var column = 0b0'u8

    for letter in boardingPass[0 .. 6]:
        # F 70 01000110
        # B 66 01000010
        # so letter and 0b100'u8 will return 100 for F and 0 for B
        row = rotateLeftBits(row, 1) + 0b1'u8 - rotateRightBits(uint8(letter) and 0b100'u8, 2)

    for letter in boardingPass[7 .. 9]:
        # L 76 01001100
        # R 82 01010010
        # so letter and 0b10'u8 will return 10 for R and 0 for L
        column = rotateLeftBits(column, 1) + rotateRightBits(uint8(letter) and 0b10'u8, 1)

    return (row, column)

proc run(s: string): string =
    var finalId: uint16 = 0
    var currentId: uint16 = 0
    for boardingPass in s.split('\n'):
        currentId = seatId(analyze(boardingPass))
        if currentId > finalId:
            finalId = currentId
    return $finalId

var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
