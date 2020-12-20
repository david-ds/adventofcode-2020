const RECURSIVE_MAX = 5

function run(s)
    # Your code here
    lines = eachline(IOBuffer(s))
    rules = Dict{SubString,SubString{String}}()
    for line in lines
        if isempty(line)
            break
        end
        (idx, rule) = split(line, ": ", limit=2)
        if idx == "8"
            rule = "42+"[1:end]
        elseif idx == "11"
            rule = "42_31"[1:end]
        end
        rules[idx] = rule
    end
    memory = Dict{SubString{String},String}()
    function resolve_rule(rule::SubString{String})::String
        # memoize here
        get!(memory, rule) do 
            if '+' in rule
                return "(?:$(resolve_rule(rule[1:end - 1])))+"
            elseif '_' in rule
                (left, right) = split(rule, "_", limit=2)
                left_pat = resolve_rule(left)
                right_pat = resolve_rule(right)
                tmp = ("(?:$(left_pat){$(i)}$(right_pat){$(i)})" for i in 1:RECURSIVE_MAX)
                return "(?:$(join(tmp, "|")))"
            elseif '"' in rule
                return rule[2:2]
            elseif '|' in rule
                (left, right) = split(rule, " | ", limit=2)
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
