function parse_line(line::String)::Tuple{Int,Int,Char,SubString}
    lower_bound::Int = 1
    upper_bound::Int = 1
    char::Char = 'a'
    
    first_idx::Int = 1
    for (idx, c) in enumerate(line)
        if c == '-'
            lower_bound = parse(Int, SubString(line, first_idx, idx - 1))
            first_idx = idx + 1
        elseif c == ' '
            upper_bound = parse(Int, SubString(line, first_idx, idx - 1))
            char = line[idx + 1]
            first_idx = idx + 4
            break
        end    
    end
    password = SubString(line, first_idx, lastindex(line))
    return lower_bound, upper_bound, char, password
end


function run(s)
    # Your code here
    count = 0
    for line in readlines(IOBuffer(s))
        pos1, pos2, char, password = parse_line(line)
        if xor(password[pos1] == char, password[pos2] == char)
            count += 1
        end
    end
    return count
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
