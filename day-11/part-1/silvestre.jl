function parse_map(s)
    lines = readlines(IOBuffer(s))
    is_seat = falses((length(lines) + 2, length(lines[1]) + 2))
    for i in 1:length(lines)
        for j in 1:length(lines[1])
            is_seat[i + 1, j + 1] = lines[i][j] == 'L'
        end
    end
    return is_seat
end

function count_neighbors(is_occupied::BitArray{2}, i::Int, j::Int)::Int
    count::Int = 0
    for i_offset in (-1, 0, 1)
        for j_offset in (-1, 0, 1)
            if i_offset == 0 && j_offset == 0
            elseif is_occupied[i + i_offset, j + j_offset]
                count += 1
            end
        end
    end
    return count
end


function run(s)
    # Your code here
    is_seat = parse_map(s)
    is_occupied = copy(is_seat)
    old_is_occupied = copy(is_seat)
    n_rows, n_cols = size(is_seat)
    
    has_changed::Bool = true
    new_free::Bool = false
    new_occupied::Bool = false
    n_neighbors::Int = 0
    while has_changed
        # is_seat .& .!is_occupied = not_occupied
        has_changed = false
        old_is_occupied .= is_occupied
        for i in 2:n_rows - 1
            for j in 2:n_cols - 1
                if is_seat[i, j]
                    n_neighbors = count_neighbors(old_is_occupied, i, j)
                    new_occupied = is_seat[i, j] & !old_is_occupied[i, j] & (n_neighbors == 0)
                    new_free = old_is_occupied[i, j] & (n_neighbors >= 4)
                    if new_occupied
                        has_changed = true
                        is_occupied[i, j] = true
                    elseif new_free
                        has_changed = true
                        is_occupied[i, j] = false
                    end
                end
            end
        end
    end
    return sum(is_occupied)
end

#########################################

function main()
    res, time, memory = @timed run(ARGS[1])
    println("_duration:$(time * 1000)")
    println(res)
end

main()
