function count_questions(group_lines)
    counts = zeros(Int, (26))
    n_answers = 1
    for c in group_lines
        int_c = Int(c)
        if int_c == 10
            n_answers += 1
        else
            counts[int_c - 96] += 1
        end
    end
    return sum(counts .== n_answers)
end

function run(s)
    # Your code here
    return sum(count_questions(group_lines) for group_lines in split(s, "\n\n"))
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
    