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

function is_valid_ticket(values::Array{Int,1}, rules::Array{Int,2}, n_rules::Int)::Bool
    for v in values
        if !any(rules[i, 1] <= v <= rules[i, 2] for i in 1:n_rules)
            return false
        end
    end
    return true
end

function update_possibilities(possibilities::Array{Int,2}, rules::Array{Int,2}, values::Array{Int,1}, n_rules::Int)
    for row_idx in 1:n_rules
        for col_idx in 1:n_rules
            i = 2 * col_idx - 1
            if !(rules[i, 1] <= values[row_idx] <= rules[i, 2]) && !(rules[i + 1, 1] <= values[row_idx] <= rules[i + 1, 2])
                possibilities[row_idx, col_idx] = 0
            end
        end
    end
end

function run(s)
    rules::Array{Int,2} = zeros(Int, (50, 2))
    rules_mask::Array{Bool,1} = zeros(Bool, (0))
    n_rules::Int = 0
    
    mode::Int = RULES_MODE
    possibilities::Array{Int,2} = zeros(Int, (0, 0))
    myticket::Array{Int,1} = zeros(Int, (0))
    for (idx, line) in enumerate(readlines(IOBuffer(s)))
        if length(line) < 20
            if length(line) == 0
                if mode == RULES_MODE
                    possibilities = ones(Int, (n_rules, n_rules))
                end
                mode += 1
            end
            continue
        elseif mode == RULES_MODE
            add_rule(line, idx, rules)
            push!(rules_mask, startswith(line, "departure"))
            n_rules += 1
        elseif mode == MY_TICKET_MODE
            myticket = parse.(Int, split(line, ","))
            update_possibilities(possibilities, rules, myticket, n_rules)
        elseif mode == NEARBY_TICKETS_MODE
            values = parse.(Int, split(line, ","))
            if is_valid_ticket(values, rules, n_rules)
                update_possibilities(possibilities, rules, values, n_rules)
            end
        end
    end
    while sum(possibilities) > n_rules
        for col_idx in 1:n_rules
            v = view(possibilities, :, col_idx)
            if sum(v) == 1
                row_idx = argmax(v)
                possibilities[row_idx, 1:end] .= 0
                possibilities[row_idx, col_idx] = 1
            end
        end
    end
    indexes = [argmax(view(possibilities, :, col_idx)) for col_idx in 1:n_rules if rules_mask[col_idx]]
    return prod(myticket[idx] for idx in indexes) 
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
