const N_CYCLES = 6

function count_neighbors(grid::Array{Int,3}, row::Int, col::Int, layer::Int)::Int
    count::Int = 0
    for x in row - 1:row + 1
        for y in col - 1:col + 1
            for z in layer - 1:layer + 1
                if x == row && y == col && z == layer
                    continue
                else
                    count += grid[x, y, z]
                end
            end
        end
    end
    return count
end

function run(s)
    offset = N_CYCLES + 1
    grid = zeros(Int, (8 + 2 * offset, 8 + 2 * offset, 1 + 2 * offset))
    for (row, line) in enumerate(eachline(IOBuffer(s)))
        for (col, c) in enumerate(line)
            if c == '#'
                grid[row + offset, col + offset, 1 + offset] = 1
            end
        end
    end
    old_grid = copy(grid)
    n_neighbors::Int = 0
    for cycle in 1:N_CYCLES
        old_grid .= grid
        for row in offset + 1 - cycle:offset + 8 + cycle
            for col in offset + 1 - cycle:offset + 8 + cycle
                for layer in offset + 1 - cycle:offset + 1 + cycle
                    n_neighbors = count_neighbors(old_grid, row, col, layer)
                    if (old_grid[row, col, layer] != 0) && (n_neighbors != 2) && (n_neighbors != 3)
                        grid[row, col, layer] = 0
                    elseif (old_grid[row, col, layer] == 0) && (n_neighbors == 3)
                        grid[row, col, layer] = 1
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
