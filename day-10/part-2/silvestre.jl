function run(s)
    # Your code here
    joltages = readlines(IOBuffer(s))
    joltages = [parse(Int, j) for j in joltages]
    sort!(joltages)
    pushfirst!(joltages, 0)
    cache = zeros(Int, size(joltages))
    cache[1] = 1
    for i in 1:length(joltages)
        if (i - 1 > 0) && (joltages[i] - joltages[i - 1] <= 3)
            cache[i] += cache[i - 1]
        end
        if (i - 2 > 0) && (joltages[i] - joltages[i - 2] <= 3)
            cache[i] += cache[i - 2]
        end
        if (i - 3 > 0) && (joltages[i] - joltages[i - 3] <= 3)
            cache[i] += cache[i - 3]
        end
    end
    return cache[end]
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
