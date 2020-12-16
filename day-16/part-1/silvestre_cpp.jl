const MAX_RANGES = 50

struct Range
    from::Int
    to::Int
end

function parse_split(line::String, sep::Char)
    ret = Int[]
    i::Int = 1
    j::Union{Nothing,Int} = findnext(sep, line, i + 1)
    while j !== nothing
        push!(ret, parse(Int, SubString(line, i, j - 1)))
        i = j + 1
        j = findnext(sep, line, i + 1)
    end
    push!(ret, parse(Int, SubString(line, i, lastindex(line))))
    return ret
end

function add_range(line::String, line_idx::Int, ranges::Array{Range,1})
    idx1 = findnext(':', line, 1) + 1
    idx2 = findnext('-', line, idx1 + 1) - 1
    idx3 = idx2 + 2
    idx4 = findnext(' ', line, idx3 + 1) - 1
    ranges[2 * line_idx - 1] = Range(
        parse(Int, SubString(line, idx1, idx2)),
        parse(Int, SubString(line, idx3, idx4))
    )
    idx1 = idx4 + 5
    idx2 = findnext('-', line, idx1 + 1) - 1
    idx3 = idx2 + 2
    idx4 = lastindex(line)
    ranges[2 * line_idx] = Range(
        parse(Int, SubString(line, idx1, idx2)),
        parse(Int, SubString(line, idx3, idx4))
    )
end

function is_valid(value::Int, ranges::Array{Range,1}, n_ranges::Int)::Bool
    return any(ranges[i].from <= value <= ranges[i].to for i in 1:n_ranges)
end

function run(s)
    ranges = Array{Range,1}(undef, MAX_RANGES)
    n_ranges::Int = 0
    
    counter::Int = 0
    lines = eachline(IOBuffer(s))
    for line in lines
        if isempty(line)
            break
        end
        n_ranges += 1
        add_range(line, n_ranges, ranges)
    end
    for line in lines
        if isempty(line)
            break
        end
    end
    for line in Iterators.drop(lines, 1)
        values = parse_split(line, ',')
        for v in values
            if !is_valid(v, ranges, n_ranges)
                counter += v
                break
            end
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
