import os, times
import strutils

proc validate(passport: string): bool =
    var counter = 0
    var acc = ""
    var hasCID = false
    var skip = false
    for letter in passport:
        if letter == ' ' or letter == '\n':
            acc = ""
            skip = false
            continue

        if skip:
            continue

        if letter == ':':
            skip = true
            if acc == "cid":
                hasCID = true
            inc(counter)
            continue

        acc = acc & letter

    return counter == 8 or (counter == 7 and not hasCID)

proc run(s: string): string =
    var counter = 0
    for passport in s.split("\n\n"):
        if validate(passport):
            inc(counter)
    return $counter


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
