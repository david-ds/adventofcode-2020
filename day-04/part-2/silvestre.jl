function is_between(value, low, high)
    return low <= parse(Int, value) <= high
end

function is_valid_height(value)
    if endswith(value, "cm")
        return is_between(value[1:end - 2], 150, 193)
    elseif endswith(value, "in")
        return is_between(value[1:end - 2], 59, 76)
    else
        return false
    end
end


function check_constraints(fields)
    for k in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        if !(k in keys(fields))
            return false
        end
        value = fields[k]
        if k == "byr" && !is_between(value, 1920, 2002)
            return false
        elseif k == "iyr" && !is_between(value, 2010, 2020)
            return false
        elseif k == "eyr" && !is_between(value, 2020, 2030)
            return false
        elseif k == "hgt" && !is_valid_height(value)
            return false
        elseif k == "hcl" && !occursin(r"^#[0-9a-f]{6}$", value)
            return false
        elseif k == "ecl" && !(value in Set(("amb", "blu", "brn", "gry", "grn", "hzl", "oth")))
            return false
        elseif k == "pid" && !occursin(r"^[0-9]{9}$", value)
            return false
        end
    end
    return true
end

function run(s)
    # Your code here
    passports = split(s, "\n\n")
    counter = 0
    for passport_str in passports
        fields = split(replace(passport_str, '\n' => ' '), ' ')
        fields = Dict(map(x -> split(x, ":"), fields))
        if check_constraints(fields)
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
