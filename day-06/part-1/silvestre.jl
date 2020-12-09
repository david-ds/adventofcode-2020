function count_questions(group_lines)
    return length(Set(replace(group_lines, '\n' => "")))
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
