module Test

export run

function update_mask(line, one_mask, zero_mask)
    one_mask = 0
    zero_mask = 0
    for idx in 1:36
        if line[7 + idx] == '1'
            one_mask |= 1 << (36 - idx)
        elseif line[7 + idx] == '0'
            zero_mask |= 1 << (36 - idx)
        end
    end
    return (zero_mask, one_mask)
end

function run(s)
    # Your code here
    one_mask::Int = 0
    zero_mask::Int = 0
    memory = Dict{Int,Int}()
    addr::Int = 0
    value::Int = 0
    for line in readlines(IOBuffer(s))
        if line[2] == 'a'
            (zero_mask, one_mask) = update_mask(line, one_mask, zero_mask)
        else
            parts = split(line, " = ", limit=2)
            addr = parse(Int, SubString(parts[1], 5, lastindex(parts[1]) - 1))
            value = parse(Int, parts[2])
            memory[addr] = (value | one_mask) & ~zero_mask 
        end
    end
    return sum(values(memory))
end

end 

#########################################
using .Test: run

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
