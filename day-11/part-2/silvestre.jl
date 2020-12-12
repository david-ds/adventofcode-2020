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

function get_neighbor_seats(is_seat)
    n_seats = sum(is_seat)
    n_rows, n_cols = size(is_seat)
    neighbor_seats = zeros(Int, (n_seats, 8, 2))
    directions = [
        # north
        (-1, 0),
        # north-west
        (-1, 1),
        # west
        (0, 1),
        # south-west
        (1, 1),
        # south
        (1, 0),
        # south-east
        (1, -1),
        # east
        (0, -1),
        # north-east
        (-1, -1)
    ]
    k = 0
    for i in 2:n_rows - 1
        for j in 2:n_cols - 1
            if is_seat[i, j]
                k += 1
                for (d_idx, (d_i, d_j)) in enumerate(directions)
                    x, y = i + d_i, j + d_j
                    while !(is_seat[x, y]) && (1 < x < n_rows) && (1 < y < n_cols)
                        x += d_i
                        y += d_j
                    end
                    neighbor_seats[k, d_idx, :] = [x, y]
                end
            end
        end
    end
    return neighbor_seats
end

function count_neighbors(is_occupied::BitArray{2}, neighbor_seats::Array{Int,3}, k::Int)::Int
    count::Int = 0
    x::Int = 0
    y::Int = 0
    for d_idx in 1:8
        x = neighbor_seats[k, d_idx, 1]
        y = neighbor_seats[k, d_idx, 2]
        if is_occupied[x, y]
            count += 1
        end
    end
    return count
end

function run(s)
    # Your code here
    is_seat = parse_map(s)
    neighbor_seats = get_neighbor_seats(is_seat)
    is_occupied = copy(is_seat)
    old_is_occupied = copy(is_seat)
    n_rows, n_cols = size(is_seat)
    
    has_changed::Bool = true
    new_free::Bool = false
    new_occupied::Bool = false
    n_neighbors::Int = 0
    k::Int = 0
    while has_changed
        # is_seat .& .!is_occupied = not_occupied
        has_changed = false
        k = 0
        old_is_occupied .= is_occupied
        for i in 2:n_rows - 1
            for j in 2:n_cols - 1
                if is_seat[i, j]
                    k += 1
                    n_neighbors = count_neighbors(old_is_occupied, neighbor_seats, k)
                    new_occupied = is_seat[i, j] & !old_is_occupied[i, j] & (n_neighbors == 0)
                    new_free = old_is_occupied[i, j] & (n_neighbors >= 5)
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
