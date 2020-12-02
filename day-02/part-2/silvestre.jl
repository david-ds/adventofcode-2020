function parse_line(line)
    rule, password = split(line, ": ")
    counts, char = split(rule, " ")
    char = char[1] # convert to Char
    pos1, pos2 = map(x -> parse(Int, x), split(counts, "-"))
    return pos1, pos2, char, password
end

function run(s)
    # Your code here
    entries = split(s, "\n")
    count = 0
    for line in entries
        pos1, pos2, char, password = parse_line(line)
        if xor(password[pos1] == char, password[pos2] == char)
            count += 1
        end
    end
    return count
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
