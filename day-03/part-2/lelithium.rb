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
    [
        run_slope(s, 1, 1),
        run_slope(s, 3, 1),
        run_slope(s, 5, 1),
        run_slope(s, 7, 1),
        run_slope(s, 1, 2)
    ].reduce(&:*)
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
