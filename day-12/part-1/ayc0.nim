from times import cpuTime
from os import paramStr
import strutils

type Direction = enum north = 0, east = 1, south = 2, west = 3
type Rotation = enum left = -1, right = 1

type Coord = object
    x: int
    y: int


proc rotate(direction: Direction, rotation: Rotation, angle: int): Direction =
    var stableAngle = (angle div 90) %% 4
    if stableAngle == 0:
        return direction
    var newDirection = (int(direction) + stableAngle * int(rotation)) %% 4
    return Direction(newDirection)



proc run(s: string): int =
    # Your code here
    var direction = Direction.east
    var coord = Coord(x: 0, y: 0)

    var lines = strip(s).split("\n")
    for line in lines:
        var modifier = line[0]
        var amount = parseInt(line[1 .. line.len - 1])

        if modifier == 'L':
            direction = rotate(direction, left, amount)
        elif modifier == 'R':
            direction = rotate(direction, right, amount)
        elif modifier == 'N' or (modifier == 'F' and direction == north):
            coord.y += amount
        elif modifier == 'S' or (modifier == 'F' and direction == south):
            coord.y -= amount
        elif modifier == 'E' or (modifier == 'F' and direction == east):
            coord.x += amount
        elif modifier == 'W' or (modifier == 'F' and direction == west):
            coord.x -= amount

    return abs(coord.x) + abs(coord.y)


var input: string = paramStr(1)
# var input = """F10
# N3
# F7
# R90
# F11"""

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
