function run(s::String)::Int
    # Your code here
    numbers = Dict{Int,Int}()
    
    # init numbers
    prev_idx::Int = 1
    idx::Union{Int,Nothing} = findnext(',', s, prev_idx)
    n_starting_numbers::Int = 1
    while idx !== nothing
        numbers[parse(Int, SubString(s, prev_idx, idx - 1))] = n_starting_numbers
        n_starting_numbers += 1
        prev_idx = idx + 1
        idx = findnext(',', s, prev_idx)
    end

    last_seen_number::Int = parse(Int, SubString(s, prev_idx, lastindex(s)))
    current_number::Int = 0
    for idx::Int in n_starting_numbers:30000000 - 1
        current_number = idx - get(numbers, last_seen_number, idx)
        numbers[last_seen_number] = idx
        last_seen_number = current_number
    end
    return last_seen_number
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
