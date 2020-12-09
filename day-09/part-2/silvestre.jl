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
    # find invalid number
    invalid_number = 0
    for idx in 26:length(numbers)
        s = numbers[idx]
        if !check(numbers, idx)
            invalid_number = numbers[idx]
            break
        end
    end

    # find matching sequence
    i = 1
    j = 2
    s = sum(numbers[i:j])
    while s != invalid_number
        if s < invalid_number
            j += 1
            s += numbers[j]
        else
            s -= numbers[i]
            i += 1
        end
    end
    return minimum(numbers[i:j]) + maximum(numbers[i:j])
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
