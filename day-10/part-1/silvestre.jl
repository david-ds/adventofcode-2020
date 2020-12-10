function run(s)
    # Your code here
    joltages = readlines(IOBuffer(s))
    joltages = [parse(Int, j) for j in joltages]
    sort!(joltages)
    pushfirst!(joltages, 0)
    diffs = joltages[2:end] - joltages[1:end - 1]
    return sum(diffs .== 1) * (sum(diffs .== 3) + 1)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
