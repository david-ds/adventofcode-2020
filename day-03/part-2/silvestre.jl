using Printf

function parse_map(s)
    lines = split(s, "\n")
    map_arr = zeros(Bool, length(lines), length(lines[1]))
    for (row_idx, l) in enumerate(lines)
        for (col_idx, c) in enumerate(l)
            map_arr[row_idx, col_idx] = (c == '#')
        end
    end
    return map_arr
end

function count_trees_on_slope(map_arr, right, down)
    tree_counter = 0
    x, y = 1, 1
    n_rows, n_cols = size(map_arr)
    while x <= n_rows
        if map_arr[x, y]
            tree_counter += 1
        end
        x += down
        y = (y + right) % n_cols
        if y == 0
            y = n_cols
        end
    end
    return tree_counter
end

function run(s)
    # Your code here
    map_arr = parse_map(s)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    results = map(x -> count_trees_on_slope(map_arr, x...), slopes)
    return reduce(*, results)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
