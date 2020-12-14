function update_mask(line, one_mask, x_mask)
    one_mask = 0
    x_mask = 0
    for idx in 1:36
        if line[7 + idx] == '1'
            one_mask |= 1 << (36 - idx)
        elseif line[7 + idx] == 'X'
            x_mask |= 1 << (36 - idx)
        end
    end
    return (one_mask, x_mask)
end

function store(memory::Dict{Int,Int}, base_addr::Int, value::Int, x_mask::Int)
    addr = base_addr & ~x_mask
    memory[addr] = value
    max_addr = base_addr | x_mask
    while addr < max_addr
        for idx in 36:-1:1
            c = (1 << (36 - idx))
            if x_mask & c != 0
                if addr & c == 0
                    zero_mask = (c - 1) & addr  & x_mask
                    addr = (addr | c) & ~zero_mask
                    break
                end
            end
        end
        memory[addr] = value
    end
end

function run(s)
    # Your code here
    one_mask::Int = 0
    x_mask::Int = 0
    memory = Dict{Int,Int}()
    addr::Int = 0
    value::Int = 0
    for line in readlines(IOBuffer(s))
        if startswith(line, "mask")
            (one_mask, x_mask) = update_mask(line, one_mask, x_mask)
        else
            parts = split(line, " = ")
            addr = parse(Int, SubString(parts[1], 5, lastindex(parts[1]) - 1)) 
            addr |= one_mask
            value = parse(Int, parts[2])
            store(memory, addr, value, x_mask)
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
