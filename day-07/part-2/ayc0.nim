from times import cpuTime
from os import paramStr
from strutils import split, parseInt, strip
import tables

type Bag = object
    quantity: int
    content: ref seq[Bag]

type RefContent = ref (seq[Bag])

var bags: array[0..593, RefContent]
var cache = newTable[string, int]()

var i = 0

proc getContent(color: string): RefContent =
    if cache.hasKey(color):
        return bags[cache[color]]
    var content = new RefContent
    cache[color] = i
    bags[i] = content
    inc(i)
    return content

proc parseLine(line: string): void =
    var lineMatch = line.split(" bags contain ")
    var content = getContent(lineMatch[0])
    var contentChunks = lineMatch[1]
    if contentChunks == "no other bags.":
        return
    for contentChunk in contentChunks.split(", "):
        var contentMatch = contentChunk.split(" ", maxsplit = 1)
        var quantity = parseInt(contentMatch[0])
        var color = contentMatch[1].split(" bag", maxsplit = 1)[0]
        var subContent = getContent(color)
        var bag = Bag(quantity: quantity, content: subContent)
        content[].add(bag)

proc getNb(content: RefContent): int =
    var count = 1
    for child in content[]:
        count = count + child.quantity * getNb(child.content)
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
