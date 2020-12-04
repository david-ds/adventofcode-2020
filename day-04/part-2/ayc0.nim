import os, times
import strutils
# from sequtils import map

proc byr(s: string): bool =
    try:
        var n = parseInt(s)
        return n >= 1920 and n <= 2002
    except ValueError:
        return false

proc iyr(s: string): bool =
    try:
        var n = parseInt(s)
        return n >= 2010 and n <= 2020
    except ValueError:
        return false

proc eyr(s: string): bool =
    try:
        var n = parseInt(s)
        return n >= 2020 and n <= 2030
    except ValueError:
        return false

proc hgt(s: string): bool =
    var unit = s[s.len - 2 .. s.len - 1]
    try:
        var n = parseInt(s[0 .. s.len - 3])
        if unit == "in":
            return n >= 59 and n <= 76
        if unit == "cm":
            return n >= 150 and n <= 193
        return false
    except ValueError:
        return false

proc hcl(s: string): bool =
    if s.len != 7:
        return false
    if s[0] != '#':
        return false
    for l in s[1 .. s.len - 1]:
        if l != '0' and l != '1' and l != '2' and l != '3' and l != '4' and l != '5' and l != '6' and l != '7' and l != '8' and l != '9' and l != 'a' and l != 'b' and l != 'c' and l != 'd' and l != 'e' and l != 'f':
            return false
    return true

proc ecl(s: string): bool =
    return s == "amb" or s == "blu" or s == "brn" or s == "gry" or s == "grn" or s == "hzl" or s == "oth"

proc pid(s: string): bool =
    if s.len != 9:
        return false
    for l in s:
        if l != '0' and l != '1' and l != '2' and l != '3' and l != '4' and l != '5' and l != '6' and l != '7' and l != '8' and l != '9':
            return false
    return true

proc cid(s: string): bool =
    return true

proc validateField(field: string, value: string): bool =
    if field == "byr":
        return byr(value)
    if field == "iyr":
        return iyr(value)
    if field == "eyr":
        return eyr(value)
    if field == "hgt":
        return hgt(value)
    if field == "hcl":
        return hcl(value)
    if field == "ecl":
        return ecl(value)
    if field == "pid":
        return pid(value)
    if field == "cid":
        return cid(value)
    return false

proc validate(passport: string): bool =
    var counter = 0
    var accField = ""
    var accValue = ""
    var hasField = false
    var hasCID = false
    for letter in passport & '\n':
        if letter == ' ' or letter == '\n':
            if accField == "cid":
                hasCID = true
            if validateField(accField, accValue):
                inc(counter)
            accField = ""
            accValue = ""
            hasField = false
            continue

        if letter == ':':
            hasField = true
            continue

        if hasField:
            accValue = accValue & letter
        else:
            accField = accField & letter

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
