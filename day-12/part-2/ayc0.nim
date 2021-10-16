from times import cpuTime
from os import paramStr
import strutils

type Rotation = enum left = -1, right = 1

type Coord = object
    x: int
    y: int


proc rotateWaypoint(coord: Coord, rotation: Rotation, angle: int): Coord =
    var stableAngle = (angle div 90) %% 4
    if stableAngle == 0:
        return coord
    var change = (stableAngle * int(rotation)) %% 4
    if change == 1:
        # rotate right
        return Coord(x: coord.y, y: -coord.x)
    if change == 2:
        # turn around
        return Coord(x: -coord.x, y: -coord.y)
    if change == 3:
        # turn left
        return Coord(x: -coord.y, y: coord.x)



proc run(s: string): int =
    # Your code here
    var boatCoord = Coord(x: 0, y: 0)
    var waypointCoord = Coord(x: 10, y: 1)

    var lines = strip(s).split("\n")
    for line in lines:
        var modifier = line[0]
        var amount = parseInt(line[1 .. line.len - 1])

        if modifier == 'N':
            waypointCoord.y += amount
        elif modifier == 'S':
            waypointCoord.y -= amount
        elif modifier == 'E':
            waypointCoord.x += amount
        elif modifier == 'W':
            waypointCoord.x -= amount

        elif modifier == 'L':
            waypointCoord = rotateWaypoint(waypointCoord, left, amount)
        elif modifier == 'R':
            waypointCoord = rotateWaypoint(waypointCoord, right, amount)

        else:
            boatCoord.x += waypointCoord.x * amount
            boatCoord.y += waypointCoord.y * amount


    return abs(boatCoord.x) + abs(boatCoord.y)


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
