function run(s)
    lines = split(s, "\n")
    timestamp = parse(Int, lines[1])
    minutes = [parse(Int, el) for el in split(lines[2], ",") if el != "x"]
    chosen::Int = -1
    waiting_time::Int = -1
    for m in minutes
        wt = m - timestamp % m
        if (wt < waiting_time) || (waiting_time < 0)
            waiting_time = wt
            chosen = m
        end
    end
    return waiting_time * chosen
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
