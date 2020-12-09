function check(numbers, idx)
    for i in idx - 25:idx - 2
        for j in i:idx - 1
            if numbers[i] + numbers[j] == numbers[idx]
                return true
            end
        end
    end
    return false
end


function run(s)
    numbers = readlines(IOBuffer(s))
    numbers = [parse(Int, n) for n in numbers]
    for idx in 26:length(numbers)
        s = numbers[idx]
        if !check(numbers, idx)
            return numbers[idx]
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
