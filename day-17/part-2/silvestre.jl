const N_CYCLES = 6

function count_neighbors(grid::Array{Int,4}, x0::Int, y0::Int, z0::Int, w0::Int)::Int
    count::Int = 0
    for x in x0 - 1:x0 + 1
        for y in y0 - 1:y0 + 1
            for z in z0 - 1:z0 + 1
                for w in w0 - 1:w0 + 1
                    if x == x0 && y == y0 && z == z0 && w == w0
                        continue
                    else
                        count += grid[x, y, z, w]
                    end
                end
            end
        end
    end
    return count
end

function run(s)
    offset = N_CYCLES + 1
    grid = zeros(Int, (8 + 2 * offset, 8 + 2 * offset, 1 + 2 * offset, 1 + 2 * offset))
    for (row, line) in enumerate(eachline(IOBuffer(s)))
        for (col, c) in enumerate(line)
            if c == '#'
                grid[row + offset, col + offset, 1 + offset, 1 + offset] = 1
            end
        end
    end
    old_grid = copy(grid)
    n_neighbors::Int = 0
    for cycle in 1:N_CYCLES
        old_grid .= grid
        for x in offset + 1 - cycle:offset + 8 + cycle
            for y in offset + 1 - cycle:offset + 8 + cycle
                for z in offset + 1 - cycle:offset + 1 + cycle
                    for w in offset + 1 - cycle:offset + 1 + cycle
                        n_neighbors = count_neighbors(old_grid, x, y, z, w)
                        if (old_grid[x, y, z, w] != 0) && (n_neighbors != 2) && (n_neighbors != 3)
                            grid[x, y, z, w] = 0
                        elseif (old_grid[x, y, z, w] == 0) && (n_neighbors == 3)
                            grid[x, y, z, w] = 1
                        end
                    end
                end
            end
        end
    end 
    return sum(grid)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
