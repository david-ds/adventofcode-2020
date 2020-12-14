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
        if startswith(line, "mask")
            (zero_mask, one_mask) = update_mask(line, one_mask, zero_mask)
        else
            idx = findfirst('=', line)
            addr = parse(Int, SubString(line, 5, idx - 3))
            value = parse(Int, SubString(line, idx + 2, lastindex(line)))
            memory[addr] = (value | one_mask) & ~zero_mask 
        end
    end
    return sum(values(memory))
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
