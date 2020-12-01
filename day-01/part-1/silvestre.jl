function run(s)
    # Your code here
    entries = split(s, "\n")
    entries = map(x -> parse(Int, x), entries)
    for el1 in entries
        for el2 in entries
            if el1 + el2 == 2020
                return el1 * el2 
            end
        end
    end
    return 0
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time*1000)")
    println(res)
end

main()
