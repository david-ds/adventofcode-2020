function run(s)
    lines = split(s, "\n")
    constraints = [(idx, parse(Int, el)) for (idx, el) in enumerate(split(lines[2], ",")) if el != "x"]
    ts::Int = 0
    jump::Int = 1
    current_idx::Int = 1
    max_idx = length(constraints)
    while true
        offset, mul = constraints[current_idx]
        if (ts + (offset - 1)) % mul == 0
            current_idx += 1
            jump *= mul
        end
        if current_idx > max_idx
            return ts
        end
        ts += jump
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
