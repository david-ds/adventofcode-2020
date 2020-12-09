function format_inner(inner)
    first_index = findfirst(isequal(' '), inner) + 1
    last_index = findlast(isequal(' '), inner) - 1
    return inner[first_index:last_index]
end

function parse_rules(s)
    rules = Dict{String,Vector{String}}()
    for line in readlines(IOBuffer(s))
        outer, inners = split(line, " bags contain ")
        if inners == "no other bags."
            continue
        end
        for inner in split(inners, ", ")
            formatted_inner = format_inner(inner)
            if formatted_inner in keys(rules)
                push!(rules[formatted_inner], outer)
            else
                rules[formatted_inner] = [outer,]
            end
        end
    end
    return rules
end
function fill_can_be_included_in(rules, bag, acc)
    push!(acc, bag)
    if bag in keys(rules)
        for next in rules[bag]
            if !(next in acc)
                fill_can_be_included_in(rules, next, acc)
            end
        end
    end
end

function run(s)
    # Your code here
    rules = parse_rules(s)
    
    acc = Set()
    fill_can_be_included_in(rules, "shiny gold", acc)
    return length(acc) - 1
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
