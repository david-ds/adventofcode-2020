function check(fields, required_fields)
    return all(f in fields for f in required_fields)
end

function run(s)
    # Your code here
    passports = split(s, "\n\n")
    counter = 0
    required_fields = Set(
        ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    )
    for passport_str in passports
        fields = split(replace(passport_str, '\n' => ' '), ' ')
        fields = map(x -> split(x, ":")[1], fields)
        if check(fields, required_fields)
            counter += 1
        end
    end
    return counter
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
