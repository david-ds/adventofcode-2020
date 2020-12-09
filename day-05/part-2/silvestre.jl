function seat_id(line)
    arr::Array{Int} = [x in ('B', 'R') ? 1 : 0 for x in line]
    return sum([x * 2^(n - 1) for (n, x) in enumerate(arr[end:-1:1])])
end

function run(s)
    # Your code here
    seat_ids = sort([seat_id(line) for line in split(s, '\n')])
    for idx in 1:length(seat_ids)
        if seat_ids[idx + 1] != seat_ids[idx] + 1
            return seat_ids[idx] + 1
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
