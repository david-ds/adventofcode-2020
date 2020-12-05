from times import cpuTime
from os import paramStr
from strutils import split
from bitops import rotateLeftBits

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
        row = rotateLeftBits(row, 1)
        if letter == 'B':
            row = row + 0b1'u8

    for letter in boardingPass[7 .. 9]:
        column = rotateLeftBits(column, 1)
        if letter == 'R':
            column = column + 0b1'u8

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
