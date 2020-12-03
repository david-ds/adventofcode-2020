import os, times

type Dimensions = tuple
    horizontal: int
    vertical: int

type Slope = tuple
    horizontal: int
    vertical: int

proc getDimensions(map: string): Dimensions =
    var horizontal = 0
    for x in map:
        inc(horizontal)
        if x == '\n':
            break
    var vertical = map.len div horizontal
    return (horizontal, vertical)

proc getTrees(map: string, dimensions: Dimensions, slope: Slope): int =
    var i = 0
    var j = 0
    var counter = 0
    var pos = 0
    while i <= dimensions.vertical:
        pos = i * dimensions.horizontal + j %% (dimensions.horizontal - 1)
        if map[pos] == '#':
            inc(counter)
        i += slope.vertical
        j += slope.horizontal
    return counter

proc run(s: string): string =
    # Your code here
    var dimensions = getDimensions(s)
    return $(
        getTrees(s, dimensions, (horizontal: 1, vertical: 1)) *
        getTrees(s, dimensions, (horizontal: 3, vertical: 1)) *
        getTrees(s, dimensions, (horizontal: 5, vertical: 1)) *
        getTrees(s, dimensions, (horizontal: 7, vertical: 1)) *
        getTrees(s, dimensions, (horizontal: 1, vertical: 2))
    )


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
