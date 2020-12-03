def run(s)
    cur_x = 0
    cur_y = 0
    s.map(&:chomp).each.with_index.inject(0) do |trees, (line, cur_y)|
        if cur_y % 1 == 0
            if line[cur_x % 31] == "#"
                trees += 1
            end
            cur_x += 3
        end
        trees
    end
end


starting = Process.clock_gettime(Process::CLOCK_MONOTONIC)
answer = run(ARGV[0].lines)
elapsed = (Process.clock_gettime(Process::CLOCK_MONOTONIC) - starting) * 1000

puts "_duration:#{elapsed}\n#{answer}"
