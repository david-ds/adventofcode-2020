function execute_code(code)
    acc = 0
    curr = 1
    seen = Set{Int}()
    while curr != length(code) + 1
        if curr in seen
            return nothing
        end
        push!(seen, curr)
        op, arg = code[curr]
        if op == "acc"
            curr += 1
            acc += arg
        elseif op == "jmp"
            curr += arg
        else
            curr += 1
        end
    end
    return acc
end

function run(s)
    # Your code here
    code = readlines(IOBuffer(s))
    code = [(line[1:3], parse(Int, line[5:end])) for line in code]
    for (idx, (op, arg)) in enumerate(code)
        if op == "acc"
            continue
        elseif op == "jmp"
            code[idx] = ("nop", arg)
        else
            code[idx] = ("jmp", arg)
        end
        acc = execute_code(code)
        if acc === nothing
            code[idx] = (op, arg)
        else
            return acc
        end
    end
    return 0
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
