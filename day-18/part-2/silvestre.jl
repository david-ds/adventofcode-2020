const ADD = 0
const MUL = 1

function evaluate(line::String, i::Int, linelength::Int)::Tuple{Int,Int}
    res::Vector{Int} = [0]
    op::Int = 0
    while i <= linelength
        if line[i] == ' '
            i += 1
        elseif line[i] == '*'
            op = MUL
            i += 2
        elseif line[i] == '+'
            op = ADD
            i += 2
        elseif line[i] == '('
            (tmp, i) = evaluate(line, i + 1, linelength)
            if op == ADD
                res[end] += tmp
            elseif op == MUL
                push!(res, tmp)
            end
        elseif line[i] == ')'
            return (prod(res), i + 1)
        else
            tmp = parse(Int, line[i])
            if op == ADD
                res[end] += tmp
            elseif op == MUL
                push!(res, tmp)
            end
            i += 1
        end
    end
    return (prod(res), i)
end


function run(s)
    counter::Int = 0
    for line in eachline(IOBuffer(s))
        (res, _) = evaluate(line, 1, lastindex(line))
        counter += res
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
