function run(s::String)::Int
    # Your code here
    numbers = Dict{Int,Int}()
    
    start = parse.(Int, split(s, ","))

    for idx in 1:length(start)
        numbers[start[idx]] = idx
    end
    
    last_seen_number::Int = start[end]
    current_number::Int = 0
    for idx::Int in length(start):2020 - 1
        if haskey(numbers, last_seen_number)
            current_number = idx - numbers[last_seen_number]
            numbers[last_seen_number] = idx
        else
            current_number = 0
            numbers[last_seen_number] = idx
        end
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
