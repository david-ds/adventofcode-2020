function run(s)
    # Your code here
    x::Int, y::Int = 0, 0
    dir::Int = 0
    for line in readlines(IOBuffer(s))
        action = line[1]
        value = parse(Int, line[2:end])
        if action == 'N'
            y += value
        elseif action == 'E'
            x += value
        elseif action == 'S'
            y -= value
        elseif action == 'W'
            x -= value
        elseif action == 'L'
            dir = (dir + value) % 360
        elseif action == 'R'
            dir = (dir - value + 360) % 360
        elseif action == 'F'
            if dir == 0
                x += value
            elseif dir == 90
                y += value
            elseif dir == 180
                x -= value
            elseif dir == 270
                y -= value
            else
                error("unknown direction")
            end
        end
    end
    return abs(y) + abs(x)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
