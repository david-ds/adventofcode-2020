function run(s)
    # Your code here
    code = readlines(IOBuffer(s))
    seen = Set{Int}()
    curr = 1
    acc = 0
    while !(curr in seen)
        push!(seen, curr)
        line = code[curr]
        op = line[1:3]
        if op == "acc"
            acc += parse(Int, line[5:end])
            curr += 1
        elseif op == "jmp"
            curr += parse(Int, line[5:end])
        else
            curr += 1
        end
    end
    return acc
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
