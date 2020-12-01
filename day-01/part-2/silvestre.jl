function run(s)
    # Your code here    
    entries = split(s, "\n")
    entries = map(x -> parse(Int, x), entries)
    for (idx1, el1) in enumerate(entries)
        for (idx2, el2) in enumerate(entries[idx1+1:end])
            if el1 + el2 > 2020
                continue
            end
            for el3 in entries[idx1+idx2+1:end]
                if el1 + el2 + el3 == 2020
                    return el1 * el2 * el3
                end
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
