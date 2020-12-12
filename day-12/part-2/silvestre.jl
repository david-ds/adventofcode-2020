function rotate(value, wp_x, wp_y)
    if value == 90
        wp_x, wp_y = -wp_y, wp_x
    elseif value == 180
        wp_x, wp_y = -wp_x, -wp_y
    elseif value == 270
        wp_x, wp_y = wp_y, - wp_x
    else
        error("unknown value")
    end
    return wp_x, wp_y
end

function run(s)
    # Your code here
    x::Int, y::Int = 0, 0
    wp_x::Int, wp_y::Int = 10, 1
    for line in readlines(IOBuffer(s))
        action = line[1]
        value = parse(Int, line[2:end])
        if action == 'N'
            wp_y += value
        elseif action == 'E'
            wp_x += value
        elseif action == 'S'
            wp_y -= value
        elseif action == 'W'
            wp_x -= value
        elseif action == 'L'
            wp_x, wp_y = rotate(value % 360, wp_x, wp_y)
        elseif action == 'R'
            wp_x, wp_y = rotate((-value + 360) % 360, wp_x, wp_y)
        elseif action == 'F'
            x += value * wp_x
            y += value * wp_y
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
