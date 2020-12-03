def run_slope(s, skip_x, skip_y)
    trees = 0
    cur_x = 0
    cur_y = 0
    s.map(&:chomp).each_with_index do |line, cur_y|
        if cur_y % skip_y == 0
            if line[cur_x % 31] == "#"
                trees += 1
            end
            cur_x += skip_x
        end
    end
    trees
end

def run(s)
    trees = [0, 0, 0, 0, 0]
    slopes = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2],
    ]
    cur = [0, 0, 0, 0, 0]
    s.map(&:chomp).each_with_index do |line, cur_y|
        slopes.each_with_index do |(skip_x, skip_y), i|
            if cur_y % skip_y == 0
                if line[cur[i] % 31] == "#"
                    trees[i] += 1
                end
                cur[i] += skip_x
            end
        end
    end
    trees.reduce(&:*)
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
