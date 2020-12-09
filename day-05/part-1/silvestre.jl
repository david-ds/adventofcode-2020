function seat_id(line)
    arr::Array{Int} = [x in ('B', 'R') ? 1 : 0 for x in line]
    return sum([x * 2^(n - 1) for (n, x) in enumerate(arr[end:-1:1])])
end

function run(s)
    # Your code here
    return maximum(seat_id(line) for line in split(s, '\n'))
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
