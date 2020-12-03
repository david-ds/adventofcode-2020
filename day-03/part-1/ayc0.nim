import os, times

type Dimensions = tuple
    horizontal: int
    vertical: int

proc getDimensions(s: string): Dimensions =
    var horizontal = 0
    for x in s:
        inc(horizontal)
        if x == '\n':
            break
    var vertical = s.len div horizontal
    return (horizontal, vertical)

proc run(s: string): string =
    # Your code here
    var dimensions = getDimensions(s)
    var i = 0
    var j = 0
    var counter = 0
    var pos = 0
    while i <= dimensions.vertical:
        pos = i * dimensions.horizontal + j %% (dimensions.horizontal - 1)
        if s[pos] == '#':
            inc(counter)
        i += 1
        j += 3
    return $counter


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
