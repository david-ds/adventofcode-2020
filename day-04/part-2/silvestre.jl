function is_between(value::String, low::Int, high::Int)::Bool
    return low <= parse(Int, value) <= high
end

function is_valid_height(value::String)::Bool
    if endswith(value, "cm")
        return is_between(value[1:end - 2], 150, 193)
    elseif endswith(value, "in")
        return is_between(value[1:end - 2], 59, 76)
    else
        return false
    end
end


function check_constraints(fields::Dict{String,String})::Bool
    required_fields = Set{String}(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))
    if !(issubset(required_fields, keys(fields)))
        return false
    elseif !is_between(fields["byr"], 1920, 2002)
        return false
    elseif !is_between(fields["iyr"], 2010, 2020)
        return false
    elseif !is_between(fields["eyr"], 2020, 2030)
        return false
    elseif !is_valid_height(fields["hgt"])
        return false
    elseif !occursin(r"^#[0-9a-f]{6}$", fields["hcl"])
        return false
    elseif !(fields["ecl"] in Set{String}(("amb", "blu", "brn", "gry", "grn", "hzl", "oth")))
        return false
    elseif !occursin(r"^[0-9]{9}$", fields["pid"])
        return false
    end
    return true
end

function run(s::String)::Int
    # Your code here
    passports::Array{String} = split(s, "\n\n")
    counter::Int = 0
    for passport_str in passports
        tags::Array{String} = split(replace(passport_str, '\n' => ' '), ' ')
        fields = Dict{String,String}(map(x -> split(x, ":"), tags))
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
