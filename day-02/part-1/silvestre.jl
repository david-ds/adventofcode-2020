function parse_line(line)
    rule, password = split(line, ": ")
    counts, char = split(rule, " ")
    char = char[1] # convert to Char
    lower_bound, upper_bound = map(x -> parse(Int, x), split(counts, "-"))
    return lower_bound, upper_bound, char, password
end

function count_char(char, string)
    counter = 0
    for c in string
        if c == char
            counter += 1
        end
    end
    return counter
end

function run(s)
    # Your code here
    entries = split(s, "\n")
    count = 0
    for line in entries
        lower_bound, upper_bound, char, password = parse_line(line)
        if lower_bound <= count_char(char, password) <= upper_bound
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
