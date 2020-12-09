function parse_rules(s)
    rules = Dict{String,Vector{Tuple{String,Int}}}()
    for line in readlines(IOBuffer(s))
        outer, inners = split(line, " bags contain ")
        if startswith(inners, "no other bags.")
            continue
        end
        inners = string(inners)
        inners = replace(inners, r"(bags?|\.)" => "")
        for inner in split(inners, ", ")
            parts = split(strip(inner), ' ', limit=2)
            n = parse(Int, parts[1])
            formatted_inner = parts[2]
            if outer in keys(rules)
                push!(rules[outer], (formatted_inner, n))
            else
                rules[outer] = [(formatted_inner, n),]
            end
        end
    end
    return rules
end

function fill_can_be_included_in(rules, bag, factor)
    acc::Int = 0
    if bag in keys(rules)
        for (next, n) in rules[bag]
            acc += n * factor
            if next in keys(rules)
                acc += fill_can_be_included_in(rules, next, n * factor)
            end
        end
    end
    return acc
end

function run(s)
    # Your code here
    rules = parse_rules(s)
    return fill_can_be_included_in(rules, "shiny gold", 1)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
