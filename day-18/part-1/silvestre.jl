const ADD = 0
const MUL = 1

function evaluate(line::String, i::Int, linelength::Int)::Tuple{Int,Int}
    res::Int = 0
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
                res += tmp
            elseif op == MUL
                res *= tmp
            end
        elseif line[i] == ')'
            return (res, i + 1)
        else
            if op == ADD
                res += parse(Int, line[i])
            elseif op == MUL
                res *= parse(Int, line[i])
            end
            i += 1
        end
    end
    return (res, i)
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
