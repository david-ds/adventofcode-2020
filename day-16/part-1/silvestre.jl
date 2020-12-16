const RULES_MODE = 0
const MY_TICKET_MODE = 1
const NEARBY_TICKETS_MODE = 2


function add_rule(line::String, line_idx::Int, rules::Array{Int,2})
    first_idx = findnext(':', line, 1) + 1
    second_idx = findnext('-', line, first_idx + 1) - 1
    rules[2 * line_idx - 1, 1] = parse(Int, SubString(line, first_idx, second_idx))
    first_idx = second_idx + 2
    second_idx = findnext(' ', line, first_idx + 1) - 1
    rules[2 * line_idx - 1, 2] = parse(Int, SubString(line, first_idx, second_idx))
    first_idx = second_idx + 5
    second_idx = findnext('-', line, first_idx + 1) - 1
    rules[2 * line_idx, 1] = parse(Int, SubString(line, first_idx, second_idx))
    first_idx = second_idx + 2
    second_idx = lastindex(line)
    rules[2 * line_idx, 2] = parse(Int, SubString(line, first_idx, second_idx))
end

function is_valid(value::Int, rules::Array, n_rules::Int)::Bool
    return any(rules[i, 1] <= value <= rules[i, 2] for i in 1:n_rules)
end

function run(s)
    rules = zeros(Int, (50, 2))
    n_rules::Int = 0
    
    counter::Int = 0
    mode::Int = RULES_MODE
    for line in readlines(IOBuffer(s))
        if length(line) < 20
            if length(line) == 0
                mode += 1
            end
            continue
        elseif mode == RULES_MODE
            n_rules += 1
            add_rule(line, n_rules, rules)
        elseif mode == NEARBY_TICKETS_MODE
            values = parse.(Int, split(line, ","))
            for v in values
                if !is_valid(v, rules, n_rules)
                    counter += v
                    break
                end
            end
        end
    end
    return counter
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
