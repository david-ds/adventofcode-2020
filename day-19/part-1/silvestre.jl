function run(s)
    # Your code here
    lines = eachline(IOBuffer(s))
    rules = Dict{SubString, SubString}()
    for line in lines
        if isempty(line)
            break
        end
        (idx, rule) = split(line, ": ", limit=2)
        rules[idx] = rule
    end
    memory = Dict{SubString,String}()
    function resolve_rule(rule::SubString)::String
        # memoize here
        get!(memory, rule) do
            if '"' in rule
                return rule[2:2]
            elseif '|' in rule
                left, right = split(rule, " | ")
                return "(?:$(resolve_rule(left))|$(resolve_rule(right)))"
            else
                parts = split(rule, " ")
                return join((resolve_rule(rules[i]) for i in parts), "")
            end 
        end
    end

    regex_str = resolve_rule(rules["0"])
    regex = Regex("^$(regex_str)\$")
    return sum(occursin.(regex, lines))
end

#########################################

function main()
    run(ARGS[1])
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
