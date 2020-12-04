function check(fields::Set{String}, required_fields::Set{String})::Bool
    return issubset(required_fields, fields)
end

function run(s::String)::Int
    # Your code here
    passports::Array{String} = split(s, "\n\n")
    counter::Int = 0
    required_fields::Set{String} = Set{String}(
        ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
    )
    for passport_str in passports
        tags::Array{String} = split(replace(passport_str, '\n' => ' '), ' ')
        fields::Set{String} = Set{String}(map(x -> split(x, ':')[1], tags))
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
