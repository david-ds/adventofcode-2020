from times import cpuTime
from os import paramStr
from strutils import split, strip
import tables

type Bag = object
    color: string
    isIncludedIn: seq[ref Bag]
    isCounted: bool

type BagRef* = ref Bag

var bags: array[0..594, BagRef]
var cache = newTable[string, int]()

var i = 0

proc getBag(color: string): BagRef =
    if cache.hasKey(color):
        return bags[cache[color]]
    var bag = BagRef(color: color)
    cache[color] = i
    bags[i] = bag
    inc(i)
    return bag

proc parseLine(line: string): void =
    var lineMatch = line.split(" bags contain ")
    var bag = getBag(lineMatch[0])
    var contentChunks = lineMatch[1]
    if contentChunks == "no other bags.":
        return
    for contentChunk in contentChunks.split(", "):
        var contentMatch = contentChunk.split(" ", maxsplit = 1)
        var color = contentMatch[1].split(" bag", maxsplit = 1)[0]
        var subBag = getBag(color)
        subBag.isIncludedIn.add(bag)

proc getNb(bag: BagRef): int =
    if bag.isCounted:
        return 0
    bag.isCounted = true
    var count = 1
    for parent in bag.isIncludedIn:
        count = count + getNb(parent)
    return count


proc run(s: string): string =
    var rows = s.strip().split('\n')
    for row in rows:
        parseLine(row);
    return $(getNb(bags[cache["shiny gold"]]) - 1)


var input: string = paramStr(1)

var t0 = cpuTime()
var output = run(input)

echo "_duration:", (cpuTime() - t0) * 1000
echo output
